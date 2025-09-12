in 01
mov B, A
mvi A, 0 ; writes 0 to register A

F1:
 inr A ; increment register A
 call delayB
 out 04 ; for debug purpose. out 04  outputs A to output reg 04
 jmp f1 ; jumps to f1

delayB:
 mov C, A
 mov A, B
decLoop:
 dcr A
 jnz decLoop
 in 01
 mov B, A
 mov A, C
 ret
