.global _start
_start:
.intel_syntax noprefix
    push rdx
    pop rsi

    push rax
    pop rdi

    syscall
    