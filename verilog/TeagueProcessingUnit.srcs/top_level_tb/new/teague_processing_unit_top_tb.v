`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 08:32:23 PM
// Design Name: 
// Module Name: teague_processing_unit_top_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module teague_processing_unit_top_tb(

    );
    
    reg clk;
    wire [15:0] debug;
    wire [15:0] program;
    wire [15:0] alu;
    wire [15:0] debug_reg;
    wire [15:0] cp_val_out;
    wire pending_setval_out;
    wire setval_out;
    wire [5:0] pending_write_address;
    
    teague_processing_unit_top DUT(
        .clk(clk),
        .debug(debug),
        .program(program),
        .alu_reg(alu),
        .debug_reg(debug_reg),
        .cp_val_out(cp_val_out),
        .pending_setval_out(pending_setval_out),
        .setval_out(setval_out),
        .pending_write_addr(pending_write_address)
    );
    
    always # 10 clk <= ~clk;
    
    initial begin
        clk <= 0;
        # 100000 $finish;
    end
endmodule
