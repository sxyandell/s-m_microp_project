// Minimal example top: performs one MCP4725 write after reset.
// Configure addr_7b to 7'h60 (A0=0) or 7'h61 (A0=1).
// Tie to UPduino clock, map SDA/SCL pins in constraints, add external pull-ups.
module mcp4725_example_top #(
  parameter int unsigned SYS_CLK_HZ = 12_000_000,
  parameter int unsigned I2C_CLK_HZ = 100_000,
  parameter logic [6:0]  ADDR_7B    = 7'h60,
  parameter logic [11:0] DAC_CODE   = 12'h800
) (
  input  logic clk,     // e.g., 12 MHz on UPduino
  input  logic rst_n,   // active-low reset
  inout  tri   i2c_sda,
  inout  tri   i2c_scl
);

  // Fire a single write after reset deasserts
  typedef enum logic [1:0] {W_IDLE, W_ARM, W_GO, W_DONE} wst_e;
  wst_e wst, wst_n;

  logic start_pulse;
  logic busy, done, nack_any;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      wst <= W_IDLE;
    end else begin
      wst <= wst_n;
    end
  end

  always_comb begin
    wst_n = wst;
    start_pulse = 1'b0;
    unique case (wst)
      W_IDLE: wst_n = W_ARM;
      W_ARM:  begin
        start_pulse = 1'b1;  // single-cycle pulse
        wst_n = W_GO;
      end
      W_GO:   if (done) wst_n = W_DONE;
      W_DONE: wst_n = W_DONE;
      default: wst_n = W_IDLE;
    endcase
  end

  i2c_mcp4725_write #(
    .SYS_CLK_HZ(SYS_CLK_HZ),
    .I2C_CLK_HZ(I2C_CLK_HZ)
  ) u_wr (
    .clk       (clk),
    .rst_n     (rst_n),
    .sda       (i2c_sda),
    .scl       (i2c_scl),
    .addr_7b   (ADDR_7B),
    .dac_code  (DAC_CODE),
    .start     (start_pulse),
    .busy      (busy),
    .done      (done),
    .nack_any  (nack_any)
  );

endmodule


