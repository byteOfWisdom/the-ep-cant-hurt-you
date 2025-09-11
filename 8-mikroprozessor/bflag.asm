mvi B, 16 ; 4th bit is set

loop:
 mvi A, 16 ; moves the relevant bitmask into A
 ana B
 cnz turnOn
 mov E, A ; out 04 ist korrekt für später
 mvi B, 0 ; in B
 jmp loop

turnOn:
 mvi A, 255
 ret
