"""Add exam blueprint supplemental cards to cover all challenging concepts and commands."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# These are cards directly from the exam blueprint "Challenging Concepts" and "Commands to Know"
# Each card is one concept, one answer - following good flashcard principles.

SUPPLEMENT = [
    # === Licensing & Open Source ===
    {"section":"1.3","type":"concept","front":"Name the 4 main characteristics of the GNU GPL License","back":"1. Freedom to run the program\n2. Freedom to study/modify source code\n3. Freedom to redistribute copies\n4. Freedom to distribute modified versions\nAll derivatives must also be GPL (copyleft)."},
    {"section":"1.3","type":"concept","front":"What are the 2 main license categories?","back":"Copyleft (GNU GPL) — derivatives must keep same license.\nPermissive (Apache, BSD, MIT) — derivatives can use any license."},
    {"section":"1.3","type":"concept","front":"What does 'Free as in freedom, not free as in beer' mean?","back":"Open source 'free' refers to liberty (freedom to use, modify, share) — not zero cost. You can charge money for free software."},
    {"section":"1.3","type":"concept","front":"What is Creative Commons used for?","back":"Putting control back into the hands of the author. Lets creators choose exactly which rights to reserve and which to waive for their creative works."},
    
    # === Applications ===
    {"section":"1.2","type":"concept","front":"GIMP","back":"Linux image editing application (raster/bitmap graphics)."},
    {"section":"1.2","type":"concept","front":"Inkscape","back":"Linux vector graphics editor (SVG format)."},
    {"section":"1.2","type":"concept","front":"Blender","back":"Linux 3D animation and modeling application."},
    {"section":"1.2","type":"concept","front":"Apache and NGINX","back":"Linux web server applications. Apache (httpd) is the most widely deployed; NGINX excels at reverse proxy and high concurrency."},
    {"section":"1.2","type":"concept","front":"Where is the OS stored on a Raspberry Pi?","back":"On the SD card (microSD). The Raspberry Pi boots from the SD card, not an internal hard drive."},
    
    # === Shell & Filesystem Basics ===
    {"section":"2.3","type":"concept","front":"What do '.' and '..' represent in the filesystem?","back":"'.' = current directory\n'..' = parent directory"},
    {"section":"2.1","type":"concept","front":"Why is the space character significant to the shell?","back":"The shell uses spaces as argument delimiters. A filename with spaces is interpreted as multiple arguments unless quoted or escaped with backslash."},
    {"section":"2.3","type":"concept","front":"Why are Windows file extensions meaningless to Linux?","back":"Linux determines file type by content (magic bytes), not extension. The 'file' command inspects content. Extensions are just conventions for humans."},
    {"section":"2.1","type":"concept","front":"How do you wrap a long command in the terminal?","back":"Use a backslash (\\) at the end of the line. This escapes the newline and continues the command on the next line."},
    {"section":"2.2","type":"concept","front":"What are linked pages in the 'info' command called?","back":"Nodes. Info documentation is organized as a tree of nodes you navigate between."},
    {"section":"2.3","type":"concept","front":"Absolute path vs relative path","back":"Absolute: starts from / (root), e.g., /home/user/file\nRelative: starts from current directory, e.g., ../user/file\nAbsolute works from anywhere; relative depends on pwd."},
    
    # === FHS ===
    {"section":"4.3","type":"concept","front":"/home in the FHS","back":"Contains user home directories. Each user gets /home/username. Stores personal files, configs (.bashrc, .profile)."},
    {"section":"4.3","type":"concept","front":"/proc filesystem","back":"Pseudo-virtual filesystem. Contains runtime system info as files (CPU info, running processes, kernel parameters). Not real files on disk."},
    {"section":"4.3","type":"concept","front":"/sys filesystem","back":"Pseudo-virtual filesystem exposing kernel device/driver info. Used for hardware configuration and info."},
    {"section":"4.3","type":"concept","front":"/dev filesystem","back":"Contains device files. Block devices (sda, sdb), character devices (tty), and special files (/dev/null, /dev/zero)."},
    {"section":"4.3","type":"concept","front":"Where do you find documentation for installed packages?","back":"/usr/share/doc/ — contains README files, changelogs, and examples for installed packages."},
    
    # === Archiving & Compression ===
    {"section":"3.1","type":"concept","front":"Does tar compress by default?","back":"No. tar only archives (bundles files). You must add -z (gzip), -j (bzip2), or -J (xz) for compression. zip compresses by default."},
    {"section":"3.1","type":"concept","front":"tar -c, -x, -t, -f options","back":"-c = create archive\n-x = extract archive\n-t = list contents\n-f = specify filename (must be last flag before filename)\nOrder: tar -czf archive.tar.gz files"},
    {"section":"3.1","type":"concept","front":"tar compression flags: -z, -j, -J","back":"-z = gzip (.tar.gz)\n-j = bzip2 (.tar.bz2)\n-J = xz (.tar.xz)\nSpeed: gzip fastest, xz slowest\nCompression: xz best, gzip least"},
    {"section":"3.1","type":"concept","front":"Default compression level for gzip/zip","back":"Level 6 (on a scale of 1-9). -1 is fastest/least compression, -9 is slowest/most compression. -0 means no compression."},
    
    # === Search & Find ===
    {"section":"3.2","type":"concept","front":"When to use find vs locate vs grep?","back":"find: search by filename/attributes in real-time (slow but current)\nlocate: search filename index (fast but may be stale)\ngrep: search file CONTENTS for text patterns\nUpdate locate index: sudo updatedb"},
    
    # === I/O Redirection ===
    {"section":"3.2","type":"concept","front":"STDIN, STDOUT, STDERR file descriptors","back":"STDIN = 0 (standard input)\nSTDOUT = 1 (standard output)\nSTDERR = 2 (standard error)\nRedirect: > (stdout), 2> (stderr), &> (both), < (stdin)"},
    
    # === Networking ===
    {"section":"4.4","type":"concept","front":"DNS record types to know","back":"A = IPv4 address\nAAAA = IPv6 address\nMX = mail server\nCNAME = alias\nNS = name server\nPTR = reverse lookup"},
    {"section":"4.4","type":"concept","front":"DNS query commands","back":"host, dig, nslookup — all query DNS servers.\nDNS configured in /etc/resolv.conf (nameserver entries)."},
    
    # === Hardware ===
    {"section":"4.2","type":"concept","front":"Typical bus types for hard drives","back":"SATA — most common for consumer drives\nSAS — enterprise/server drives\nNVMe — fastest, connects via PCIe\nIDE/PATA — legacy (older systems)"},
    {"section":"4.1","type":"concept","front":"3 components of any Linux distribution","back":"1. Linux kernel\n2. GNU core utilities/software packages\n3. Package management system"},
    
    # === Distributions ===
    {"section":"1.1","type":"concept","front":"Debian family distros","back":"Debian (stable server) → Ubuntu Server (stable)\nUbuntu/Mint (desktop/consumer)\nKALI (ethical hacking/pentesting)\nPackage format: .deb"},
    {"section":"1.1","type":"concept","front":"Red Hat family distros","back":"Fedora (upstream) → RHEL → CentOS, Oracle Linux, Scientific Linux (downstream)\nPackage format: .rpm"},
    {"section":"1.1","type":"concept","front":"Ubuntu release cycle","back":"Releases: twice yearly (April, October) e.g., 22.04, 22.10\nLTS: every 2 years (even years only, e.g., 22.04)\nLTS support: 5 years"},
    {"section":"1.1","type":"concept","front":"What is a 'rolling release' distro?","back":"Continually updated after installation — no major version upgrades. Examples: KALI Linux, openSUSE Tumbleweed, Arch Linux."},
    {"section":"1.2","type":"concept","front":"Debian vs Red Hat package managers","back":"Debian: dpkg (low-level), apt/apt-get/aptitude (high-level)\nRed Hat: rpm (low-level), yum/dnf (high-level)\nSUSE: rpm format via zypper"},
    
    # === Users & Security ===
    {"section":"5.1","type":"concept","front":"UID of root and first standard user","back":"root = UID 0\nFirst standard user = UID 1000 (on most modern distros)"},
    {"section":"5.1","type":"concept","front":"/etc/passwd vs /etc/shadow","back":"/etc/passwd: user account info (readable by all) — username:x:UID:GID:comment:home:shell\n/etc/shadow: encrypted passwords (root only) — !! means account is locked"},
    {"section":"5.1","type":"concept","front":"How can a standard user run the passwd command?","back":"The passwd binary has the SUID (Set User ID) bit set. This means it executes with root's permissions regardless of who runs it."},
    {"section":"5.1","type":"concept","front":"Difference: '#' vs '/' vs '/root' vs 'root' user","back":"# = root prompt (vs $ for normal user)\n/ = filesystem root directory\n/root = root user's home directory\nroot = the superuser account (UID 0)"},
    {"section":"5.3","type":"concept","front":"What is umask?","back":"Sets default permissions for new files/directories. Subtracts from full permissions (666 for files, 777 for dirs). umask 022 → files get 644, dirs get 755."},
    {"section":"5.3","type":"concept","front":"Sticky bit and /tmp","back":"/tmp has the sticky bit set (chmod +t, shown as 't' in permissions: drwxrwxrwt). Prevents users from deleting files they don't own, even though /tmp is world-writable."},
    {"section":"5.3","type":"concept","front":"How to change user and group of a file","back":"chown user:group filename\nchown user filename (user only)\nchgrp group filename (group only)\n-R flag for recursive"},
    
    # === Commands from blueprint ===
    {"section":"2.1","type":"command","front":"$ export greeting=hello","back":"Creates an environment variable available to child processes. Without export, variable is local to current shell only."},
    {"section":"2.1","type":"command","front":"$ unset greeting","back":"Removes/deletes a shell variable or environment variable."},
    {"section":"5.2","type":"command","front":"$ useradd -m newuser","back":"Creates a new user account. -m creates the home directory. -M skips home dir creation. -d specifies custom home path."},
    {"section":"5.2","type":"command","front":"$ groupadd developers","back":"Creates a new group."},
    {"section":"5.3","type":"command","front":"$ umask 022","back":"Sets default permission mask. New files get 644 (666-022), new directories get 755 (777-022)."},
    {"section":"5.1","type":"command","front":"$ chsh -s /bin/zsh","back":"Changes the login shell for the current user."},
    {"section":"4.3","type":"command","front":"$ pstree","back":"Displays running processes as a tree showing parent-child relationships."},
    {"section":"4.3","type":"command","front":"$ journalctl -k","back":"Shows kernel messages from the systemd journal (equivalent to dmesg)."},
    {"section":"4.3","type":"command","front":"$ free -h","back":"Displays memory usage (RAM and swap) in human-readable format."},
    {"section":"4.3","type":"command","front":"$ lscpu","back":"Displays CPU architecture information (cores, threads, model, MHz)."},
    {"section":"4.3","type":"command","front":"$ lsblk -f","back":"Lists block devices with filesystem type, label, UUID, and mount point."},
    {"section":"4.3","type":"command","front":"$ uptime","back":"Shows how long the system has been running, number of users, and load averages."},
    {"section":"5.1","type":"command","front":"$ last","back":"Shows listing of last logged-in users from /var/log/wtmp."},
    {"section":"4.4","type":"command","front":"$ ss -t","back":"Shows active TCP socket connections (modern replacement for netstat)."},
    {"section":"3.2","type":"command","front":"$ sudo updatedb","back":"Forces an update of the locate command's file database. Required after adding/removing files for locate to find them."},
    {"section":"2.1","type":"command","front":"$ which nano","back":"Shows the full path of a command's executable (searches $PATH)."},
    {"section":"3.2","type":"command","front":"$ cut -d':' -f1 /etc/passwd","back":"Extracts field 1 from /etc/passwd using ':' as delimiter. -d sets delimiter, -f selects fields."},
    {"section":"5.3","type":"command","front":"$ ln -s target linkname","back":"Creates a symbolic (soft) link. The link points to the target file/directory. -s means symbolic (without -s creates hard link)."},
    {"section":"4.3","type":"command","front":"$ dmesg | grep boot","back":"Shows kernel ring buffer messages filtered for boot-related entries."},
    {"section":"4.3","type":"command","front":"$ top","back":"Interactive process viewer. Press M=sort by memory, P=sort by CPU, N=sort by PID, T=sort by time."},
]

# Load existing structured data
with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add supplement to each section
for card in SUPPLEMENT:
    sec_id = card['section']
    if sec_id not in data:
        continue
    if card['type'] == 'concept':
        data[sec_id]['concepts'].append({'term': card['front'], 'definition': card['back']})
    elif card['type'] == 'command':
        cmd = card['front'].replace('$ ', '')
        data[sec_id]['commands'].append({'command': cmd, 'context': card['back']})

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added {len(SUPPLEMENT)} supplemental cards from exam blueprint")
print(f"  Concepts: {sum(1 for c in SUPPLEMENT if c['type']=='concept')}")
print(f"  Commands: {sum(1 for c in SUPPLEMENT if c['type']=='command')}")
