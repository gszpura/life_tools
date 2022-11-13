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
    ; init: our program address in ds and es registers
    ; sp is a stack pointer; ss is a stack register
    mov ax, 0x7c0
    mov ds, ax
    mov es, ax
    mov ax, 0x00
    mov ss, ax
    mov sp, 0x7c00
    sti ; interupts turn on again
    mov si, message
    call print

    ; interupts example: interupt nr 0 is in 0x00,0x02 addresses in RAM
    ; we have offset:segment (offset is at 0x00, segment at 0x02)
    ; interupt 0 is invoked when we divide by 0
    mov word[ss:0x00], print_int
    mov word[ss:0x02], 0x7c0
    ; uncomment to divide by zero, print_int should be executed
    ;mov ax, 0
    ;div ax
    ;clc -clears CF flag; does not help for below code when uncommented
    ;int 0 ; other than that we can just call interupt 0x00
    
    mov ah, 02h
    mov al, 1
    mov ch, 0
    mov cl, 2
    mov dh, 0
    mov bx, buffer 
    int 0x13
    jc error ; jump and call error if CF=1 (so we have an error)

    mov si, buffer
    call print
    jmp $

error:
    mov si, error_message
    call print
    jmp $

print_int:
    mov ah, 0eh
    mov al, 'O'
    ;mov bh, 0
    int 0x10
    mov ah, 0eh
    mov al, 'K'
    int 0x10
    iret

print:
    mov bh, 0
.loop:
    lodsb ; loads one char from al register and increments pointer to point to new char
    cmp al, 0 ; compares al register to 0 i.e. end of the string
    je .done ; if cmp correct jump to done
    call print_char
    jmp .loop
.done:
    ret

print_char:
    mov ah, 0eh
    int 0x10
    ret

error_message:
    db 'Error Greg', 0

message:
    db 'Hello Greg', 0

times 510-($ - $$) db 0
dw 0xAA55

buffer: