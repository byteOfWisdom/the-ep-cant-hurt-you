mvi A, 0 ; writes 0 to register A
mvi B, 32 ; writes 64 to register B. sets period
mvi E, 32

loop:
 XRI 255 ; flip register A
 call delayB
 out 04 ; mov E, A  for debug purpose. out 04  outputs A to output reg 04
 jmp loop ; jumps to f1

delayB:
 mov C, A
 mov A, B
 ADD E
decLoop:
 dcr A
 jnz decLoop
 mov B, A
 mov A, C
 ret
