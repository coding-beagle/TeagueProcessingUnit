# Reg Bank

Inputs:

| Port Name | Width  | Purpose                                                           |
| --------- | ------ | ----------------------------------------------------------------- |
| Enable    | 1      | Toggle the outputs of this bank (Outputs will be Z on not Enable) |
| Addr A    | [5:0]  | Get the value of the read only output                             |
| Addr B    | [5:0]  | Get the value of the writable output                              |
| Value     | [15:0] | Value to set the writable if SetVal is high                       |
| SetVal    | 1      | Set the value of Addr B to Value when this is high                |

Outputs:

| Port Name     | Width  | Purpose                                 |
| ------------- | ------ | --------------------------------------- |
| Read only out | [15:0] | Outputs the value of this bank [addr A] |
| Writable out  | [15:0] | Outputs the value of this bank [addr B] |

## Storage

Each reg bank will store 60 16 bit values, with the first writeable / readable address being Reg 4 - 63.

This is because the first four registers, 0,1,2,3 are reserved for the global special registers.
