`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 03:33:34 PM
// Design Name: 
// Module Name: alu
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


module alu(
        input wire [5:0] operation,
        input wire [15:0] incoming_data,
        input wire [15:0] accumulator_in,
        output wire [15:0] result,
        output wire overflow,
        output wire carry
    );
    
    localparam  ADD = 0,
                SUB = 1,
                BSL = 2, // bit shift left
                ARS = 3, // arithmetic right shift
                LRS = 4, // logical right shift
                 OR = 5, 
                AND = 6, 
                XOR = 7;
    
    reg [16:0] working_reg ;
    reg [15:0] result_reg;
    reg overflow_reg;
    reg carry_reg;
    
    always @* begin
        result_reg = 0;
        overflow_reg = 0;
        carry_reg = 0;
        working_reg = 0;

        case (operation)
            ADD: begin
                working_reg <= accumulator_in + incoming_data;
                result_reg <= working_reg[15:0];
                carry_reg <= working_reg[16]; 
                overflow_reg = (~(accumulator_in[15] ^ incoming_data[15])) & (result_reg[15] ^ accumulator_in[15]);
              end
            SUB: begin
                working_reg = accumulator_in - incoming_data;
                result_reg = working_reg[15:0];
                carry_reg = working_reg[16];
                overflow_reg = ((accumulator_in[15] ^ incoming_data[15])) & (result_reg[15] ^ accumulator_in[15]);
            end
            BSL: working_reg <= accumulator_in << 1;
            ARS: working_reg <= accumulator_in >>> 1;
            LRS: working_reg <= accumulator_in >> 1;
            OR: working_reg <= working_reg | incoming_data;
            AND: working_reg <= working_reg & incoming_data;
            XOR: working_reg <= working_reg ^ incoming_data;
        endcase
    end

    assign result = result_reg;
    assign overflow = overflow_reg;
    assign carry = carry_reg;
    
endmodule
