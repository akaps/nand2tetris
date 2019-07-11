// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(RESET)
    @SCREEN
    D=A
    M[pos]=D

(CHECK)
    D=M[KBD]
    @WHITE
    D;JEQ

(BLACK)
    @0 // 0-1 is 0xffff, or 16 black pixels
    D=A
    M[color]=D
    @FILL
    0;JMP

(WHITE)
    @1 // 1-1 is 0x0000, or 16 white pixels
    D=A
    M[color]=D

(FILL)
    //cool hack, thanks forums
    //We can't load 0xffff, since the msb is for the load instruction
    //Instead, get it with 0-1. In this case color is 1 for white and 0 for black
    D=M[color]-1
    @pos
    A=M
    M=D
    D=A
    @1
    D=D+A
    M[pos]=D
    @SCREEN
    D=D-A
    @8192 //32 words per row, 256 rows
    D=D-A
    @RESET
    D;JEQ
    @CHECK
    0;JMP
