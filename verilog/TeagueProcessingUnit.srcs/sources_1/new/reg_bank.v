`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 12:46:30 PM
// Design Name: 
// Module Name: reg_bank
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


module reg_bank #(parameter bank_address = 2'b01)(
        input wire clk,
        input wire rst,
        input wire bank_sel_addr,
        input wire [5:0] addr_a,
        input wire [5:0] addr_b,
        input wire [15:0] value,
        input wire setval,
        output wire [15:0] read_only_out,
        output wire [15:0] writeable_out
    );

    reg [15:0] bank [0:59];

    assign read_only_out = ( bank_sel_addr == bank_address || addr_a > 3) ? bank[addr_a - 4] : 16'bzzzzzzzzzzzzzzzz;
    assign writeable_out =  ( bank_sel_addr == bank_address || addr_b > 3) ? bank[addr_b - 4] : 16'bzzzzzzzzzzzzzzzz;

    always @ (posedge clk) begin 
        if(rst) begin : reset
            integer i;
            for (i = 0; i < 60; i = i + 1) begin
                bank[i] <= 0;
            end
        end 
        if(setval == 1) begin
            bank[addr_b] <= value;
        end
    end

endmodule
