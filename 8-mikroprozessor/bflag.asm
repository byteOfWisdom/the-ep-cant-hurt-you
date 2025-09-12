mvi B, 16 ; 4th bit is set

loop:
 in 01 ; moves the relevant bitmask into A
 ana B
 cnz turnOn
 out 01 ; mov E, A out 04 ist korrekt für später
 jmp loop

turnOn:
 mvi A, 255
 ret
