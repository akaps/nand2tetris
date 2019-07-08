// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

    //initialize sum to 0
    M[R2]=0

    //check if R0 is 0
    D=M[R0]
    @END
    D; JEQ

    //check if R1 is 0
    D=M[R1]
    @END
    D; JEQ

    D=M[R0]
    D=D-M[R1]
    @LOOP_DEC_R1
    D; JLT // R0<R1, decreasing R0 is fewer loops than R1
    //else, decreasing R1 is fewer loops than R0. Fall through

(LOOP_DEC_R0)
    //add R1 to the running total
    D=M[R1]
    D=D+M[R2]
    M[R2]=D
    //decrement R0
    D=M[R0]
    D=D-1
    @END
    D; JLE // R0 is <= 0
    M[R0]=D
    @LOOP_DEC_R0
    D; JMP

(LOOP_DEC_R1)
    //add R0 to the running total
    D=M[R0]
    D=D+M[R2]
    M[R2]=D
    //decrement R1
    D=M[R1]
    D=D-1
    @END
    D; JLE // R1 is <= 0
    M[R1]=D
    @LOOP_DEC_R1
    D; JMP

(END)
    @END
    0; JMP
