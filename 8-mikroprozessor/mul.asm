metaloop:
 mvi H, 0
 mvi L, 0
 mvi D, 0
 in 01
 mov C, A ; move content from A register to C for sequential adding
 in 00

 mulLoop:
  cpi 0
  cnz mulIter
  cpi 0
  jnz mulLoop

 mov A, L
 out 00
 mov A, H
 out 01
jmp metaloop

mulIter:
  DAD B
  dcr A
  ret
