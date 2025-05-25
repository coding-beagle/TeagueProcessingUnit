`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2025 04:45:59 PM
// Design Name: 
// Module Name: teague_processing_unit_top
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


module teague_processing_unit_top(
        input wire clk
    );
    
    // ----- instruction opcodes -----

    localparam  NOOP = 4'b0000,
                  CP = 4'b0001,
                 IMM = 4'b0010,
                 ALU = 4'b0011,
                 JMP = 4'b0100,
                 INV = 4'b0101,
              SUBBNZ = 4'b0110;
    
    reg [15:0] instruction_memory [0:511];

    reg [15:0] current_instruction;

    reg [15:0] accumulator;
    reg [15:0] program_counter;
    reg [15:0] bank_select;
    reg [15:0] cpu_flags;
    
    wire [1:0] bank_sel;
    assign bank_sel = bank_select[1:0]; // truncate because we don't plan on using that many banks yet

    wire [5:0] address_a;
    wire [5:0] address_b;
    assign address_a = current_instruction[11:6];
    assign address_b = current_instruction[5:0];

    wire [15:0] current_readable;
    wire [15:0] current_writeable;


    // ----- Power On Reset Logic -----

    wire global_reset;

    SRL16 #(.INIT(16'hFFFF)) srl_rst (  //LUT as a shift-register initialized to All ones
        .Q(global_reset),
        .A0(1'b1),                      //Address pointing to the last element in LUT
        .A1(1'b1),
        .A2(1'b1),
        .A3(1'b1),
        .CLK(clk),
        .D(1'b0)
    );

    // ----- ALU Declaration -----

    wire carry_flag;
    wire overflow_flag;
    wire [15:0] alu_result;

    alu alu(
        .operation(address_a),
        .incoming_data(current_writeable),
        .accumulator_in(accumulator),
        .result(alu_result),
        .carry(carry_flag),
        .overflow(overflow_flag)
    );

    // ----- Register Bank Logic -----

    reg [15:0] cp_val;
    reg setval;

    reg_bank #(.bank_address(0)) bank0 (
        .clk(clk),
        .rst(global_reset),
        .bank_sel_addr(bank_sel),
        .addr_a(address_a),
        .addr_b(address_b),
        .value(cp_val),
        .setval(setval),
        .read_only_out(current_readable),
        .writeable_out(current_writeable)
    );
    
    // ----- Main Clock Logic -----

    always @ (posedge clk) begin
        if(global_reset) begin
            program_counter <= 0;
            accumulator <= 0;
            bank_select <= 0;
            cpu_flags <= 0;
            current_instruction <= 0;
            setval <= 0;
            cp_val <= 0;
        end else begin
            current_instruction <= instruction_memory[program_counter];
            setval <= 0;

            case (current_instruction[15:12])
                // We can read from all special registers
                // But only write to accumulator, program counter, and bank_sel
                CP: begin : copy_block
                    reg [15:0] cp_val_next;
                    case (address_a)
                        0: cp_val_next = accumulator;
                        1: cp_val_next = program_counter;
                        2: cp_val_next = bank_select;
                        3: cp_val_next = cpu_flags;
                        default: cp_val_next = current_readable;
                    endcase 
                    setval <= 1;
                    cp_val <= cp_val_next;
                    // guard against writing to cpu_flags
                    case (address_b)
                        0: accumulator <= cp_val_next;
                        1: program_counter <= cp_val_next;
                        2: bank_select <= cp_val_next;
                    endcase 
                end

                IMM: begin
                    accumulator <= current_instruction[11:0];
                end

                ALU: begin
                    accumulator <= alu_result;
                    cpu_flags <= {14'b00000000000000, carry_flag, overflow_flag };
                end

                JMP: begin : jump_block
                    reg signed [11:0] val;
                    val = current_instruction[11:0];
                    program_counter <= program_counter + val; 
                end

                INV: begin
                    cp_val <= ~(current_writeable);
                    setval <= 1;
                end

                SUBBNZ: begin
                    if((current_readable - current_writeable) != 0) begin
                        program_counter <= current_readable;
                    end
                end

            endcase

            program_counter <= program_counter + 1;
        end
    end


    
endmodule
