@256
D=A
@SP
M=D
@Sys:Sys.init$return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys:Sys.init
0;JMP
(Sys:Sys.init$return)
(Sys:Sys.init)
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@Sys:Sys.main$return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys:Sys.main
0;JMP
(Sys:Sys.main$return)
@5
D=A
@1
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(Sys:LOOP)
@Sys:LOOP
0;JMP
(Sys:Sys.main)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@1
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@2
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@3
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
@Sys:Sys.add12$return
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys:Sys.add12
0;JMP
(Sys:Sys.add12$return)
@5
D=A
@0
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@LCL
A=M
D=A
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@2
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@3
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
A=M
D=A
@4
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
A=M
D=A+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys:Sys.add12)
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@0
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
@3
D=A
@1
AD=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG
A=M
D=A
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
A=M
D=A+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
