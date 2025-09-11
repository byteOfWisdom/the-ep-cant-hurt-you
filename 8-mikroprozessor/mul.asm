mvi A, 15 ; in 02
mov C, A ; move content from A register to L for sequential adding
mvi A, 27 ; in 01

mulLoop:
 DAD B
 dcr A
 jnz mulLoop

mov A, L
mov E, A ; out 01
mov A, H
mov D, A ; out 02
