`timescale 10ns/1ns
/////////////////////////////////////////////
// tb_shiftreg
// testbench for shiftreg.sv
/////////////////////////////////////////////

module tb_shiftreg();
	logic clk, ready_in, x_n;
	logic [50:0] shiftreg_prev, shiftreg_new;
	
	shiftreg dut(clk, ready_in, x_n, shiftreg_prev, shiftreg_new);
	
	always begin
      clk = 1'b0; #5;
      clk = 1'b1; #5;
    end
	
	// TODO: complete this tb
endmodule