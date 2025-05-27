# TeagueASM

Python Module for creating Teague Assembly for the Teague Processing Unit

This tool (will) provide a development environment for turning Teague Assembly into .hex files for the Teague Processing Unit.

## Valid TeagueASM

The current instructions in TeagueASM are:

| Name   | Opcode | Args              | Description                                                                     |
| ------ | ------ | ----------------- | ------------------------------------------------------------------------------- |
| NOOP   | 1111   | None              | Does nothing m8                                                                 |
| CP     | 0001   | A = 11:6, B = 5:0 | Sets the value in reg B to the value in reg A                                   |
| IMM    | 0010   | A = 11:0          | Sets accumulator to a                                                           |
| ALU    | 0011   | A = 11:6, B = 5:0 | Triggers an ALU command A with the value in reg B                               |
| JMP    | 0100   | A = signed 11:0   | Sets program counter to program counter + A                                     |
| INV    | 0101   | A = 5:0           | Invert all of the bits in Reg A                                                 |
| SUBBNZ | 0110   | A = 11:6, B = 5:0 | Subtract A - B, set PC to value in A if result != 0, DOES NOT MUTATE REGISTERS! |

ALU State Machine names:

| Names | Reg A  | Description                        |
| ----- | ------ | ---------------------------------- |
| ADD   | 000000 | Add reg b to accumulator           |
| SUB   | 000001 | Subtract reg b from accumulator    |
| LLS   | 000010 | Accumulator left shift             |
| ARS   | 000011 | Accumulator arithmetic right shift |
| LRS   | 000100 | Accumulator logical right shift    |
| LOR   | 000101 | Logical OR reg b with accumulator  |
| AND   | 000110 | Logical AND reg b with accumulator |
| XOR   | 000111 | Logical XOR reg b with accumulator |

Register Names:

| Names | Corresponding Reg | Description                              |
| ----- | ----------------- | ---------------------------------------- |
| ACC   | 0                 | The accumulator register                 |
| PC    | 1                 | The register holding the program counter |
| BSEL  | 2                 | The bank select register                 |
| FLGS  | 3                 | The CPU flag register                    |

## Examples of valid TeagueASM

Simple Arithmetic:

```
IMM 100 // set accumulator register to 100 
CP ACC 04 // copy value in accumulator to reg 4
IMM 520
ALU SUB 04 // Subtract the value in reg 4 with accumulator
NOOP // blaze it
```

Jumping around:

```
IMM 42
CP ACC 04
JMP 'Jump here'
ALU SUB 04 // this should get skipped
# Jump here
IMM ${69-42} // inline macro, can be used for simple arithmetic
ALU ADD 04
NOOP // result in accumulator should be 69
```
