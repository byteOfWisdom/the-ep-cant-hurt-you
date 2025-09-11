mvi A, 0 ; writes 0 to register A
mvi B, 4 ; writes 64 to register B. sets period

F1:
 inr A ; increment register A
 call delayB
 mov E, A ; for debug purpose. out 04  outputs A to output reg 04
 jmp f1 ; jumps to f1

delayB:
 mov C, A
 mov A, B
decLoop:
 dcr A
 jnz decLoop

 mov A, C
 ret
