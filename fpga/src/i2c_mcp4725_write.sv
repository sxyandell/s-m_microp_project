// Simple I2C write engine specialized for MCP4725 "Write DAC Register" (no EEPROM).
// Sends: [START] [ADDR(7b)+W] [0x40] [D11..D4] [D3..D0 << 4] [STOP]
// Open-drain behavior on SDA/SCL: drive low for '0', release (Z) for '1'.
// Externally provide pull-ups on SDA/SCL.
//
// Parameters:
// - SYS_CLK_HZ: FPGA fabric clock frequency in Hz
// - I2C_CLK_HZ: desired I2C SCL frequency in Hz (100_000 or 400_000 typical)
//
// Usage:
//   - Provide dac_code (12-bit), addr_7b (0x60 when A0=0, 0x61 when A0=1)
//   - Pulse start high for one clk to begin a transaction
//   - busy stays high during the transfer; done pulses for one clk at completion
//   - nack_any goes high if any byte was NACKed
module i2c_mcp4725_write #(
  parameter int unsigned SYS_CLK_HZ = 12_000_000,
  parameter int unsigned I2C_CLK_HZ = 100_000
) (
  input  logic        clk,
  input  logic        rst_n,
  inout  tri          sda,
  inout  tri          scl,
  input  logic [6:0]  addr_7b,     // 7'h60 (A0=0) or 7'h61 (A0=1)
  input  logic [11:0] dac_code,    // D11..D0
  input  logic        start,       // 1 clk pulse to start
  output logic        busy,        // 1 during transfer
  output logic        done,        // 1 clk pulse when finished
  output logic        nack_any     // 1 if any NACK observed in this transfer
);

  // Derived timing
  localparam int unsigned HALF_TICKS = (SYS_CLK_HZ / (I2C_CLK_HZ * 2));
  // Guard against divide-by-zero
  localparam int unsigned HALF_TICKS_SAFE = (HALF_TICKS == 0) ? 1 : HALF_TICKS;

  // Open-drain drivers
  logic sda_drive_low;
  logic scl_drive_low;
  wire  sda_in = sda;
  wire  scl_in = scl;
  assign sda = sda_drive_low ? 1'b0 : 1'bz;
  assign scl = scl_drive_low ? 1'b0 : 1'bz;

  // Transaction bytes
  logic [7:0] byte0_addr_w;   // {addr_7b, 1'b0}
  logic [7:0] byte1_ctrl;     // 8'h40  (Write DAC register, no EEPROM)
  logic [7:0] byte2_data_msb; // D11..D4
  logic [7:0] byte3_data_lsb; // D3..D0 << 4

  // FSM
  typedef enum logic [4:0] {
    ST_IDLE,
    ST_START_A,       // ensure lines high, pull SDA low while SCL high
    ST_START_B,       // pull SCL low to begin bit clocking
    ST_BIT_SETUP,     // set SDA for current bit while SCL low
    ST_BIT_SCL_HIGH,  // release SCL high; wait
    ST_BIT_SCL_LOW,   // pull SCL low; advance bit
    ST_ACK_PREP,      // release SDA before ACK
    ST_ACK_SCL_HIGH,  // clock ACK, sample SDA
    ST_ACK_SCL_LOW,   // pull SCL low, move to next byte or stop
    ST_STOP_A,        // ensure SDA low, release SCL high
    ST_STOP_B,        // release SDA high while SCL high
    ST_DONE
  } state_e;

  state_e state, next_state;

  // Byte/bit tracking
  logic [1:0] byte_index;      // 0..3
  logic [7:0] cur_byte;
  logic [2:0] bit_index;       // 7..0
  logic       cur_bit;
  logic       ack_bit;         // 0 = ACK, 1 = NACK

  // Timing counter
  logic [$clog2(HALF_TICKS_SAFE+1)-1:0] tick_cnt;
  logic half_tick; // 1 when half period elapsed

  // Edge / pulses
  logic start_d;
  logic start_pulse;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      start_d <= 1'b0;
    end else begin
      start_d <= start;
    end
  end
  assign start_pulse = start & ~start_d;

  // Precompute bytes each time start is asserted (or continuously)
  always_comb begin
    byte0_addr_w   = {addr_7b, 1'b0};
    byte1_ctrl     = 8'h40;
    byte2_data_msb = {dac_code[11:4]};
    byte3_data_lsb = {dac_code[3:0], 4'b0000};
  end

  // Tick generator (simple countdown to half period)
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      tick_cnt  <= '0;
      half_tick <= 1'b0;
    end else begin
      if (tick_cnt == 0) begin
        tick_cnt  <= HALF_TICKS_SAFE - 1;
        half_tick <= 1'b1;
      end else begin
        tick_cnt  <= tick_cnt - 1'b1;
        half_tick <= 1'b0;
      end
    end
  end

  // Sequential FSM
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state         <= ST_IDLE;
      sda_drive_low <= 1'b0;
      scl_drive_low <= 1'b0;
      byte_index    <= 2'd0;
      bit_index     <= 3'd7;
      cur_byte      <= 8'h00;
      nack_any      <= 1'b0;
      ack_bit       <= 1'b1;
      busy          <= 1'b0;
      done          <= 1'b0;
    end else begin
      done <= 1'b0; // default, pulse only when entering ST_DONE
      if (half_tick) begin
        case (state)
          ST_IDLE: begin
            sda_drive_low <= 1'b0; // release lines (expect external pull-ups)
            scl_drive_low <= 1'b0;
            byte_index    <= 2'd0;
            bit_index     <= 3'd7;
            nack_any      <= 1'b0;
            busy          <= 1'b0;
            if (start_pulse) begin
              busy          <= 1'b1;
              state         <= ST_START_A;
            end
          end

          ST_START_A: begin
            // Ensure bus idle (both high), then drive SDA low while SCL high
            sda_drive_low <= 1'b1; // SDA low (START)
            scl_drive_low <= 1'b0; // SCL released high
            // Load first byte
            cur_byte      <= byte0_addr_w;
            bit_index     <= 3'd7;
            state         <= ST_START_B;
          end

          ST_START_B: begin
            // Pull SCL low to begin bit clocking
            scl_drive_low <= 1'b1;
            state         <= ST_BIT_SETUP;
          end

          ST_BIT_SETUP: begin
            // Set SDA for current bit while SCL low
            cur_bit        <= cur_byte[bit_index];
            sda_drive_low  <= (cur_byte[bit_index] == 1'b0); // drive low for '0', release for '1'
            state          <= ST_BIT_SCL_HIGH;
          end

          ST_BIT_SCL_HIGH: begin
            // Release SCL high; wait (also allows clock stretching if needed)
            scl_drive_low <= 1'b0;
            // Next, pull SCL low again to finish the bit
            state         <= ST_BIT_SCL_LOW;
          end

          ST_BIT_SCL_LOW: begin
            // Finish the bit, pull SCL low
            scl_drive_low <= 1'b1;
            if (bit_index != 3'd0) begin
              bit_index <= bit_index - 3'd1;
              state     <= ST_BIT_SETUP;
            end else begin
              // After 8 bits, prepare for ACK
              state <= ST_ACK_PREP;
            end
          end

          ST_ACK_PREP: begin
            // Release SDA (receiver drives ACK/NACK)
            sda_drive_low <= 1'b0;
            state         <= ST_ACK_SCL_HIGH;
          end

          ST_ACK_SCL_HIGH: begin
            // Clock ACK bit
            scl_drive_low <= 1'b0; // SCL high
            // Sample SDA during SCL high: 0=ACK, 1=NACK
            ack_bit       <= sda_in;
            state         <= ST_ACK_SCL_LOW;
          end

          ST_ACK_SCL_LOW: begin
            // Pull SCL low; handle ACK result and move to next byte or stop
            scl_drive_low <= 1'b1;
            if (ack_bit) begin
              nack_any <= 1'b1;
            end
            // Decide next byte
            if (byte_index == 2'd0) begin
              byte_index <= 2'd1;
              cur_byte   <= byte1_ctrl;
              bit_index  <= 3'd7;
              state      <= ST_BIT_SETUP;
            end else if (byte_index == 2'd1) begin
              byte_index <= 2'd2;
              cur_byte   <= byte2_data_msb;
              bit_index  <= 3'd7;
              state      <= ST_BIT_SETUP;
            end else if (byte_index == 2'd2) begin
              byte_index <= 2'd3;
              cur_byte   <= byte3_data_lsb;
              bit_index  <= 3'd7;
              state      <= ST_BIT_SETUP;
            end else begin
              // All 4 bytes sent, proceed to STOP
              state <= ST_STOP_A;
            end
          end

          ST_STOP_A: begin
            // Ensure SDA low, then release SCL high
            sda_drive_low <= 1'b1;
            scl_drive_low <= 1'b0; // SCL high
            state         <= ST_STOP_B;
          end

          ST_STOP_B: begin
            // Release SDA high while SCL is high (STOP)
            sda_drive_low <= 1'b0;
            state         <= ST_DONE;
          end

          ST_DONE: begin
            busy <= 1'b0;
            done <= 1'b1;
            state <= ST_IDLE;
          end

          default: begin
            state <= ST_IDLE;
          end
        endcase
      end
    end
  end

endmodule


