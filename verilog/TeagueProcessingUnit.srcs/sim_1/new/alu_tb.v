`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 03:58:26 PM
// Design Name: 
// Module Name: alu_tb
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


module alu_tb(

    );
    
    
    reg [5:0] operation;
    reg [15:0] incoming_data;
    reg signed [15:0] accumulator;
    wire signed [15:0] result;
    wire overflow;
    wire carry;
    
    alu DUT(
        .operation(operation),
        .incoming_data(incoming_data),
        .accumulator_in(accumulator),
        .result(result),
        .overflow(overflow),
        .carry(carry)
    );
    
    initial begin
        operation <= 0;
        incoming_data <= 0;
        accumulator <= 0;
        
        // ADDITION TESTS
        # 1
        
        incoming_data <= 5;
        accumulator <= 10;
        
        # 1 
        if(result != 15) $fatal(1, "Addition was incorrect!");
        
        incoming_data <= 65000; // test overflow + carry flag
        accumulator <= 32000;
        
        # 1
        
        if(result != 31464) $fatal(1, "Large addition is wrong");
        if(carry != 1) $fatal(1, "Carry flag was not set correctly!");
        if(overflow != 0) $fatal(1, "Overflow flag was not set correctly!");
        
        // SUBTRACTION TESTS
        operation <= 1;
        
        # 1
        
        incoming_data <= 2;
        accumulator <= 10;
        
        # 1
        
        if(result != 8) $fatal(1, "Subtraction was incorrect!");
        
        incoming_data <= 30000;
        accumulator <= -30000;
        
        # 1
        
        if(overflow != 1) $fatal(1, "Overflow flag was not set correctly on overflowed subtraction!");
        # 1
        
        // Logic test cases
        operation <= 2;
        accumulator <= 64;
        
        # 1
        
        if(result != 128) $fatal(1, "Did not shift left properly!");
        operation <= 3;
        
        # 1
        
        if(result != 32) $fatal(1, "Did not shift right properly!");
        accumulator <= -64;
        
        # 1
        
        if(result != -32) $fatal(1, "Did not arithmetically shift right!");
        operation <= 4;
        accumulator <= 64;
        
        # 1
        
        if(result != 32) $fatal(1, "Did not shift right properly!");
        
        operation <= 5;
        
        incoming_data <= 21845;
        accumulator <= 43690;
        
        # 1
        
        // because we're using signed regs
        if(result != -1) $fatal(1, "Bitwise OR was incorrect!");
        operation <= 6;
        
        incoming_data <= 1;
        accumulator <= 65535;
        
        # 1
        
        if(result != 1) $fatal(1, "Bitwise AND was incorrect!");
        
        
        $display("SUCCESS! All test cases passed!");
        
        # 1
        
        operation <= 7;
        
        incoming_data <= 65535;
        accumulator <= 65535;
        
        # 1
        
        if(result != 0) $fatal(1, "Bitwise XOR was incorrect!");
        
        $finish;
    end
    
    
endmodule
