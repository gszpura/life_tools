ORG 0
BITS 16

; needed to load from usb
first_bios_param_block:
    jmp short start
    nop
; rest of the bios param block needed to load from usb
times 33 db 0

start:
    jmp 0x7c0:init_program

init_program:
    cli ; interupts turn off to not break our init
    mov ax, 0x7c0
    mov ds, ax
    mov es, ax
    mov ax, 0x00
    mov ss, ax
    mov sp, 0x7c00
    sti ; interupts turn on again
    mov si, message
    call print
    jmp $

print:
    mov bh, 0
.loop:
    lodsb
    cmp al, 0
    je .done
    call print_char
    jmp .loop
.done:
    ret

print_char:
    mov ah, 0eh
    int 0x10
    ret

message:
    db 'Hello Greg', 0

times 510-($ - $$) db 0
dw 0xAA55