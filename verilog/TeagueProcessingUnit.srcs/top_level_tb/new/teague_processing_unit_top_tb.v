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
    
    teague_processing_unit_top DUT(
        .clk(clk),
        .debug(debug),
        .program(program),
        .alu_reg(alu)
    );
    
    always # 10 clk <= ~clk;
    
    initial begin
        clk <= 0;
        # 500 $finish;
    end
endmodule
