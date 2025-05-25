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
    reg [15:0] accumulator;
    wire [15:0] result;
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
        
        
        
        
        $display("SUCCESS! All test cases passed!");
    end
    
    
endmodule
