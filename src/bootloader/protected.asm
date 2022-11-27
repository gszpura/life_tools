ORG 0x7c00
BITS 16

CODE_SEG equ gdt_code - gdt_start 
DATA_SEG equ gdt_data - gdt_start

; needed to load from usb
first_bios_param_block:
    jmp short start
    nop
; rest of the bios param block needed to load from usb
times 33 db 0

start:
    jmp 0:init_program

init_program:
    ; in 16 bit real mode
    cli 
    mov ax, 0x00
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7c00
    sti ; interupts turn on again
    ; moves further to .load_protected
    
.load_protected:
    ; loads 32 bit mode
    cli
    ; inits GDT: https://wiki.osdev.org/Global_Descriptor_Table
    lgdt[gdt_descriptor]
    mov eax, cr0
    or eax, 0x1
    mov cr0, eax
    jmp CODE_SEG:load32

;GDT
gdt_start:
gdt_null:
    dd 0x0
    dd 0x0

; offset 0x8
gdt_code:
    dw 0xffff
    dw 0      ; Base 0-15 bits
    db 0      ; Base 16-23 bits
    db 0x9a   ; acccess byte
    db 11001111b ; High 4 bit flags
    db 0      ; Base 24-31 bits

; offset 0x10
gdt_data:
    dw 0xffff
    dw 0      ; Base 0-15 bits
    db 0      ; Base 16-23 bits
    db 0x92   ; acccess byte
    db 11001111b ; High 4 bit flags
    db 0

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

[BITS 32]
load32:
    ; some init for 32bit protected mode
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov ebp, 0x00200000
    mov esp, ebp
    jmp $

times 510-($ - $$) db 0
dw 0xAA55

; for debugging: target remote | qemu-system-x86_64 -hda ./boot.bin -S -gdb stdio