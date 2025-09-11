mvi A, 0 ; writes 0 to register A
mvi B, 4 ; writes 64 to register B. sets period
mvi C, 10; max amplitude

rising:
 inr A ; increment register A
 call delayB
 mov E, A ; for debug purpose. out 04  outputs A to output reg 04 out 04
 cmp C
 jnz rising

falling:
 dcr A ; increment register A
 call delayB
 mov E, A ; for debug purpose. out 04  outputs A to output reg 04 out 04
 jnz falling
 jmp rising


delayB:
 mov D, A
 mov A, B
decLoop:
 dcr A
 jnz decLoop
 mov A, D
 cpi 0
 ret
