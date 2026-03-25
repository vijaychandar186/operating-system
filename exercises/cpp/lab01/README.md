# Lab 01 – Installing Linux in a VM / Linux Boot Process

## Objective
Understand how to install Ubuntu Linux inside a virtual machine and trace the complete Linux boot sequence from power-on to login prompt.

---

## Software Required

| Software | Purpose |
|---|---|
| VirtualBox / VMware Workstation | Hypervisor to host the VM |
| Ubuntu 22.04 LTS ISO | Guest operating system image |

---

## VM Installation Steps

1. Download Ubuntu ISO from [ubuntu.com](https://ubuntu.com/download)
2. Install VirtualBox from [virtualbox.org](https://www.virtualbox.org)
3. Click **New** → name the VM, select **Linux / Ubuntu (64-bit)**
4. Allocate **≥ 2 GB RAM** and **≥ 20 GB** virtual disk
5. Mount the ISO under **Settings → Storage → Optical Drive**
6. Start the VM and follow the Ubuntu installation wizard
7. Remove ISO after install; reboot the VM

---

## Linux Boot Process

```
Power ON
   │
   ▼
BIOS / UEFI
 POST (Power-On Self Test)
 Locates bootable device
   │
   ▼
MBR / GPT (first 512 bytes of disk)
 Loads the bootloader (GRUB stage 1)
   │
   ▼
GRUB (Grand Unified Bootloader)
 Displays boot menu
 Loads the kernel image (vmlinuz) + initrd
   │
   ▼
Linux Kernel
 Decompresses itself into RAM
 Initialises hardware drivers
 Mounts initramfs as temporary root
 Mounts real root filesystem (/)
   │
   ▼
init / systemd  (PID 1)
 Reads unit files from /etc/systemd/system/
 Starts all services in dependency order
   │
   ▼
Login (TTY or Display Manager)
```

### Boot Stages Summary

| Stage | Component | Description |
|---|---|---|
| 1 | BIOS/UEFI | Power-on self-test; locates bootable device |
| 2 | MBR/GPT | First sector; loads GRUB stage 1 |
| 3 | GRUB | Bootloader; presents kernel menu |
| 4 | Kernel (`vmlinuz`) | Decompresses; initialises drivers; mounts root FS |
| 5 | `initramfs` | Temporary in-memory root for early-boot drivers |
| 6 | `systemd` (PID 1) | Starts all services; reaches the target runlevel |
| 7 | Login | `getty` (TTY) or display manager (`gdm`, `lightdm`) |

---

## Key Files & Locations

| Path | Purpose |
|---|---|
| `/boot/vmlinuz-*` | Compressed Linux kernel image |
| `/boot/initrd.img-*` | Initial RAM disk image |
| `/boot/grub/grub.cfg` | GRUB configuration |
| `/etc/fstab` | Filesystem mount table |
| `/etc/systemd/system/` | systemd unit files |
| `/var/log/syslog` | Boot and system log |
| `journalctl -b` | View current-boot log via systemd journal |

---

## Useful Commands After Boot

```bash
uname -r               # kernel version
systemctl list-units   # all active systemd units
journalctl -b          # boot log
dmesg | head -30       # kernel ring buffer
cat /proc/cmdline      # kernel boot parameters
lsblk                  # block devices / partitions
df -h                  # filesystem usage
```
