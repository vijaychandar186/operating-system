# Lab 02 – Linux Commands: Simple & Advanced

## Objective
Learn and practise the essential Linux shell commands used for file management, process control, networking, and system information.

---

## File & Directory Commands

| Command | Description | Example |
|---|---|---|
| `pwd` | Print working directory | `pwd` |
| `ls` | List directory contents | `ls -la` |
| `cd` | Change directory | `cd /home/user` |
| `mkdir` | Create directory | `mkdir mydir` |
| `rmdir` | Remove empty directory | `rmdir mydir` |
| `touch` | Create empty file | `touch file.txt` |
| `rm` | Remove file | `rm file.txt` |
| `rm -r` | Remove directory recursively | `rm -r mydir` |
| `cp` | Copy files | `cp src.txt dst.txt` |
| `mv` | Move / rename files | `mv old.txt new.txt` |
| `cat` | Display file contents | `cat file.txt` |
| `more` | Page through file | `more file.txt` |
| `nano` | Terminal text editor | `nano file.txt` |
| `echo` | Print text / expand variables | `echo "Hello World"` |
| `man` | Manual pages | `man ls` |

---

## File Content & Search Commands

| Command | Description | Example |
|---|---|---|
| `grep` | Search text patterns | `grep "error" log.txt` |
| `find` | Find files by name/type | `find / -name "*.txt"` |
| `wc` | Count words / lines / bytes | `wc -l file.txt` |
| `diff` | Compare two files | `diff file1.txt file2.txt` |
| `sort` | Sort lines | `sort file.txt` |
| `head` | First N lines | `head -10 file.txt` |
| `tail` | Last N lines | `tail -20 file.txt` |

---

## Archive & Compression Commands

| Command | Description | Example |
|---|---|---|
| `tar cvf` | Create tar archive | `tar cvf archive.tar *.txt` |
| `tar xvf` | Extract tar archive | `tar xvf archive.tar` |
| `gzip` | Compress file (`.gz`) | `gzip file.txt` |
| `gunzip` | Decompress `.gz` | `gunzip file.txt.gz` |
| `zcat` | View gzip file without decompressing | `zcat file.txt.gz` |

---

## Disk & System Commands

| Command | Description | Example |
|---|---|---|
| `df -m` | Disk free space (MB) | `df -m` |
| `du` | Disk usage of directory | `du -sh mydir` |
| `uname -a` | Full system information | `uname -a` |
| `free -h` | Memory usage | `free -h` |
| `uptime` | System uptime & load | `uptime` |
| `cal` | Display calendar | `cal` |
| `date` | Current date and time | `date` |

---

## User & Session Commands

| Command | Description | Example |
|---|---|---|
| `whoami` | Current username | `whoami` |
| `who` | Logged-in users | `who` |
| `last` | Login history | `last -5` |
| `finger` | User information | `finger username` |
| `sudo` | Execute as superuser | `sudo apt update` |
| `history` | Command history | `history` |
| `clear` | Clear terminal screen | `clear` |

---

## Process Commands

| Command | Description | Example |
|---|---|---|
| `ps aux` | List all running processes | `ps aux` |
| `top` / `htop` | Live process monitor | `top` |
| `kill` | Send signal to process | `kill -9 PID` |
| `killall` | Kill by process name | `killall firefox` |
| `bg` / `fg` | Background / foreground job | `bg %1` |
| `jobs` | List background jobs | `jobs` |

---

## Networking Commands

| Command | Description | Example |
|---|---|---|
| `ping` | Test connectivity | `ping google.com` |
| `hostname` | Print system hostname | `hostname` |
| `ifconfig` | Network interface info | `ifconfig eth0` |
| `ip addr` | Modern IP address tool | `ip addr show` |
| `netstat -nlt` | Open listening ports | `netstat -nlt` |
| `curl` | HTTP requests | `curl https://example.com` |
| `wget` | Download files | `wget https://example.com/file` |

---

## Permissions Commands

```bash
ls -l file.txt          # view permissions
chmod 755 script.sh     # rwxr-xr-x
chmod 644 file.txt      # rw-r--r--
chmod u+x script.sh     # add execute for owner
chmod o-r file.txt      # remove read for others
chown user:group file   # change owner and group
```

### Permission Bits

```
-rwxr-xr--
 │││││││││
 ││││││││└─ others: read only
 │││││││└── others: no write
 ││││││└─── others: no execute
 │││││└──── group: read
 ││││└───── group: no write
 │││└────── group: execute
 ││└─────── owner: read
 │└──────── owner: write
 └───────── owner: execute
```

| Symbol | Octal | Meaning |
|---|---|---|
| `r` | 4 | Read |
| `w` | 2 | Write |
| `x` | 1 | Execute |
| `-` | 0 | No permission |
