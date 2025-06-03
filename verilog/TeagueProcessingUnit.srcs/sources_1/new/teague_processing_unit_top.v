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
        input wire clk,
        output wire [15:0] debug,
        output wire [15:0] program,
        output wire [15:0] alu_reg,
        output wire [15:0] debug_reg,
        output wire [15:0] cp_val_out,
        output wire pending_setval_out,
        output wire setval_out,
        output wire [5:0] pending_write_addr
    );
    
    // ----- instruction opcodes -----

    localparam  NOOP = 4'b1111,
                  CP = 4'b0001,
                 IMM = 4'b0010,
                 ALU = 4'b0011,
                 JMP = 4'b0100,
                 INV = 4'b0101,
              SUBBZ = 4'b0110;
    
    reg [15:0] instruction_memory [0:511];
    wire [15:0] current_instruction;

    reg [15:0] accumulator;
    
    assign alu_reg = accumulator;
    
    reg [15:0] program_counter;
    reg [15:0] bank_select;
    reg [15:0] cpu_flags;
    
    assign program = instruction_memory[program_counter];
    assign current_instruction = instruction_memory[program_counter];
    
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

    wire [15:0] cp_val;
    reg [15:0] cp_val_reg;
    
    reg [15:0] pending_cp_val;
    
    assign debug_reg = pending_cp_val;
    assign cp_val = pending_cp_val;
    reg setval;
    reg pending_setval;
    reg [5:0] pending_addr_a;
    reg [5:0] pending_addr_b;
    
    assign pending_write_addr = pending_addr_b;

    assign setval_out = setval;
    assign pending_setval_out = pending_setval;
    assign cp_val_out = cp_val;

    reg_bank #(.bank_address(0)) bank0 (
        .clk(clk),
        .rst(global_reset),
        .bank_sel_addr(bank_sel),
        .addr_a(pending_addr_a),
        .addr_b(pending_addr_b),
        .value(cp_val),
        .setval(setval),
        .read_only_out(current_readable),
        .writeable_out(current_writeable),
        .reg_1(debug)
    );

    // ----- Load program file -----
    initial begin : initial_block
        integer i_val;
        $readmemh("program.hex", instruction_memory);
        $display("Instruction memory contents");
        for (i_val = 0; i_val < 512; i_val = i_val + 1) begin
            if(i_val < 5)
                $display("instruction_memory[%0d] = %h", i_val, instruction_memory[i_val]);
        end
    end
    
    // ----- Main Clock Logic -----
    // Somehow I introduced some fetch-execute pipelining
    // Lmao

    always @ (posedge clk) begin
        if(global_reset) begin
            program_counter <= 0;
            accumulator <= 0;
            bank_select <= 0;
            cpu_flags <= 0;
            setval <= 0;
            cp_val_reg <= 0;
            pending_setval <= 0;
            pending_cp_val <= 0;
            pending_addr_a <= address_a;
            pending_addr_b <= address_b;
        end else begin
            
            if(pending_setval) begin
                // guard against writing to cpu_flags
                case (pending_addr_b)
                    0: begin
                        accumulator <= cp_val;
                        program_counter <= program_counter + 1;
                    end
                    1: program_counter <= cp_val;
                    2: begin
                        bank_select <= cp_val;
                        program_counter <= program_counter + 1;
                    end
                    3: program_counter <= program_counter + 1;
                    default: begin 
                        program_counter <= program_counter + 1;
                        pending_cp_val <= cp_val_reg;
                        setval <= 1;
                    end
                endcase 
                
                pending_setval <= 0;
            end else begin
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
                        
                        pending_setval <= 1;
                        cp_val_reg <= cp_val_next;
                        pending_addr_a <= address_a;
                        pending_addr_b <= address_b;
                        

                    end

                    IMM: begin
                        accumulator <= current_instruction[11:0];
                        program_counter <= program_counter + 1;
                    end

                    ALU: begin
                        accumulator <= alu_result;
                        cpu_flags <= {14'b00000000000000, carry_flag, overflow_flag };
                        program_counter <= program_counter + 1;
                    end

                    JMP: begin : jump_block
                        reg signed [11:0] val;
                        val = current_instruction[11:0];
                        program_counter <= program_counter + val; 
                    end

                    INV: begin
                        cp_val_reg <= ~(current_writeable);
                        setval <= 1;
                        program_counter <= program_counter + 1;
                    end

                    SUBBZ: begin: subbz_block
                        reg [15:0] subtraction_result;
                        subtraction_result = accumulator - current_readable;
                        accumulator <= subtraction_result;
                        if(subtraction_result == 0) begin
                            program_counter <= current_writeable;
                        end else 
                            program_counter <= program_counter + 1;
                    end

                    default: begin
                        program_counter <= program_counter + 1;
                    end

                endcase

            end
            
        end
    end


    
endmodule
