mvi A, 0 ; writes 0 to register A
mvi B, 4 ; writes 64 to register B. sets period

loop:
 inr A ; increment register A
 call delayB
 nop
 mov E, A
 jnz loop


falling:
 dcr A ; increment register A
 call delayB
 nop
 mov E, A
 jnz falling
 jmp loop


delayB:
 mov C, A
 mov A, B
decLoop:
 dcr A
 jnz decLoop
 mov A, C
 ret
