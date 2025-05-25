# ALU

The ALU Should be able to operate asynchronously

Inputs:

| Port Name      | Width  | Purpose                                                              |
| -------------- | ------ | -------------------------------------------------------------------- |
| Operation      | [5:0]  | The operation to perform on incoming reg                             |
| Incoming Reg   | [15:0] | Data to use with the operation                                       |
| Accumulator In | [15:0] | Accumulator data (so accumulator can exist in the module above this) |

Outputs:

| Port Name | Width  | Purpose                            |
| --------- | ------ | ---------------------------------- |
| Result    | [15:0] | Value to write back to accumulator |
| Overflow  | 1      | Overflow flag                      |
| Carry     | 1      | Carry flag                         |

## ALU State Machine (as described in README.md)

| Reg A   | Description                        |
| ------- | ---------------------------------- |
| 000000  | Add reg b to accumulator           |
| 000001  | Subtract reg b from accumulator    |
| 000010  | Accumulator left shift             |
| 000011  | Accumulator arithmetic right shift |
| 000100  | Accumulator logical right shift    |
| 000101  | Logical OR reg b with accumulator  |
| 000110  | Logical AND reg b with accumulator |
| 001000  | Logical XOR reg b with accumulator |
| 001001  | Reserved                           |
| 001010  | Reserved                           |
| ...     | Reserved                           |
| 1111111 | Reserved                           |
