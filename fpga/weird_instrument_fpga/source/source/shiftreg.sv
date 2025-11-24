/*
shiftreg.sv

Takes in input signal, ready signal, and past shiftreg value,
when ready signal is high, synchronously left-shifts shiftreg,
filling in LSB with input signal.

If ready is low, holds shiftreg_new constant 

Madeleine Kan
mkan@hmc.edu
Sarah Yandell
syandell@hmc.edu
23 November, 2025
*/

module shiftreg(input logic clk, ready_in,
				input logic x_n,
				input logic [50:0] shiftreg_prev,
				output logic [50:0] shiftreg_new);
	
	logic [50:0] shifted_shiftreg_prev;
	assign shifted_shiftreg_prev = shiftreg_prev << 1;
	always_ff @(posedge clk)
		if (ready_in) shiftreg_new = {shifted_shiftreg_prev[50:1], x_n};
		else shiftreg_new = shiftreg_prev;
				
endmodule