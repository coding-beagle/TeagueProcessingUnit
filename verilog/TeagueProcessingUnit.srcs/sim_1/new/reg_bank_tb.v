`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 01:56:21 PM
// Design Name: 
// Module Name: reg_bank_tb
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
// Testing strategy:
//  
// - Test resets 
// - Test enable works
//////////////////////////////////////////////////////////////////////////////////


module reg_bank_tb(

    );

    reg clk;
    reg [1:0] bank_sel;
    reg rst;
    reg [5:0] addr_a;
    reg [5:0] addr_b;
    reg [15:0] value;
    reg setval;

    wire [15:0] read_val_bank_1;
    wire [15:0] writeable_val_bank_1;

    wire [15:0] read_val_bank_2;
    wire [15:0] writeable_val_bank_2;

    reg_bank #(.bank_address(0)) DUT_1 (
        .clk(clk),
        .rst(rst),
        .bank_sel_addr(bank_sel),
        .addr_a(addr_a),
        .addr_b(addr_b),
        .value(value),
        .setval(setval),
        .read_only_out(read_val_bank_1),
        .writeable_out(writeable_val_bank_1)
    );

    reg_bank #(.bank_address(1)) DUT_2 (
        .clk(clk),
        .rst(rst),
        .bank_sel_addr(bank_sel),
        .addr_a(addr_a),
        .addr_b(addr_b),
        .value(value),
        .setval(setval),
        .read_only_out(read_val_bank_2),
        .writeable_out(writeable_val_bank_2)
    );

    always #5 clk <= ~clk;

    initial begin
        clk <= 0;
        rst <= 1;
        bank_sel <= 0;
        addr_a <= 0;
        addr_b <= 0;
        # 30 rst <= 0;
        

        # 3
        // bank sel is 1, DUT 1 should be active, DUT 2 should show z's
        if (read_val_bank_1 != 0) $fatal(1, "Bank 1 did not reset!");
        if (read_val_bank_2 != 16'bzzzzzzzzzzzzzzzz) $fatal(1, "Bank 2 is active when bank sel is 0!");


        $display("Simulation completed properly!");
        $finish;
    end


endmodule
