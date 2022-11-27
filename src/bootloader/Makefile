all:
	nasm -f bin ./protected.asm -o ./boot.bin

boot:
	nasm -f bin ./boot.asm -o ./boot.bin
	dd if=./message.txt >> ./boot.bin