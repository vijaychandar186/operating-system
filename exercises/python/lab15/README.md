# Lab 15 – File Permissions & Binary Analysis on Linux

## Objective
Understand the Linux permission model and use standard tools to perform static analysis of ELF binary files.

---

## Part A – File Permissions

### Permission Model

Every file and directory has three permission sets: **owner (u)**, **group (g)**, **others (o)**.

```
-rwxr-xr--   1   alice   dev   4096   Mar 25 10:00   script.sh
│││││││││
│││││││││
││││││└┴┴── others : r--  (read only)
│││└┴┴───── group  : r-x  (read + execute)
└┴┴──────── owner  : rwx  (full access)
│
└─ file type: - regular, d directory, l symlink, c char device, b block device
```

### Permission Bits

| Symbol | Octal | Meaning |
|---|---|---|
| `r` | 4 | Read |
| `w` | 2 | Write |
| `x` | 1 | Execute |
| `-` | 0 | No permission |

### Common `chmod` Values

| Octal | Symbolic | Typical use |
|---|---|---|
| `755` | `rwxr-xr-x` | Executable / directory |
| `644` | `rw-r--r--` | Regular file |
| `600` | `rw-------` | Private key / secret |
| `777` | `rwxrwxrwx` | Fully open (avoid in production) |

### Permission Commands

```bash
ls -l file.txt              # view permissions
chmod 755 script.sh         # set rwxr-xr-x
chmod u+x script.sh         # add execute for owner
chmod g-w file.txt          # remove write from group
chmod o-r file.txt          # remove read from others
chmod a+r file.txt          # add read for all
chown alice:dev file.txt    # change owner and group
umask 022                   # default permission mask
```

---

## Part B – Binary Analysis Tools

### Tool Overview

| Tool | Purpose |
|---|---|
| `file` | Identify file type |
| `ldd` | List shared library dependencies |
| `strings` | Extract printable strings |
| `hexdump` | View raw bytes + ASCII |
| `readelf` | Parse ELF file structure |
| `objdump` | Disassemble sections |
| `strace` | Trace system calls at runtime |
| `ltrace` | Trace library calls at runtime |
| `nm` | List symbol table (functions/variables) |
| `gdb` | Interactive debugger |

---

### 1. `file` – Identify File Type

```bash
file /bin/ls
# /bin/ls: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
#          dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, ...
```

---

### 2. `ldd` – Shared Library Dependencies

```bash
ldd /bin/ls
#   linux-vdso.so.1 (0x00007ffd...)
#   libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1
#   libc.so.6       => /lib/x86_64-linux-gnu/libc.so.6
```

---

### 3. `strings` – Extract Printable Strings

```bash
strings /bin/ls | head -20
strings -n 8 binary       # only strings ≥ 8 chars
```

---

### 4. `hexdump` – Raw Bytes

```bash
hexdump -C /bin/ls | head
# 00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
```

The first 4 bytes `7f 45 4c 46` are the **ELF magic number** (`\x7fELF`).

---

### 5. `readelf` – Parse ELF Structure

```bash
readelf -h /bin/ls    # ELF header (type, arch, entry point)
readelf -S /bin/ls    # section headers (.text, .data, .bss, ...)
readelf -l /bin/ls    # program (segment) headers
readelf -s /bin/ls    # symbol table
readelf -d /bin/ls    # dynamic linking info
```

### ELF Section Types

| Section | Contents |
|---|---|
| `.text` | Executable machine code |
| `.data` | Initialised global/static variables |
| `.bss` | Uninitialised global/static variables |
| `.rodata` | Read-only constants and strings |
| `.plt` / `.got` | Procedure Linkage Table / Global Offset Table |
| `.symtab` | Symbol table (stripped in release builds) |
| `.debug_*` | Debug information |

---

### 6. `objdump` – Disassemble

```bash
objdump -d   /bin/ls | head -40      # disassemble .text
objdump -D   /bin/ls | head -40      # disassemble all sections
objdump -D -M intel /bin/ls | head   # Intel syntax
objdump -s   /bin/ls | head          # full hex dump of all sections
```

---

### 7. `strace` – Trace System Calls

```bash
strace /bin/ls 2>&1 | head -20
strace -e openat /bin/ls            # filter to openat() only
strace -o trace.log /bin/ls        # save to file
```

---

### 8. `ltrace` – Trace Library Calls

```bash
ltrace /bin/ls 2>&1 | head -20
```

Shows function names, arguments, and return values for shared library calls.

---

### 9. `nm` – Symbol Table

```bash
nm /bin/ls | tail -20
nm -D /bin/ls             # dynamic symbols only
```

Symbol types: `T` = text (code), `D` = data, `B` = BSS, `U` = undefined (imported).

---

### 10. `gdb` – Interactive Debugger

```bash
gdb -q ./myprogram
```

```
(gdb) break main        # set breakpoint at main()
(gdb) run               # start execution
(gdb) bt                # backtrace (call stack)
(gdb) info regs         # CPU register values
(gdb) x/20x $rsp        # examine 20 hex words on the stack
(gdb) disassemble main  # disassemble a function
(gdb) next              # step over
(gdb) step              # step into
(gdb) continue          # run until next breakpoint
(gdb) quit
```
