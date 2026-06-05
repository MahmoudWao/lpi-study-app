"""Replace auto-extracted garbage cards with clean hand-written term/definition pairs."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Replace concepts and commands with CLEAN cards for every section
CLEAN = {
  "1.1": {
    "concepts": [
      ("Linux", "Open-source operating system inspired by Unix, started by Linus Torvalds in 1991"),
      ("Linux Distribution", "Bundle of Linux kernel + software packages + package manager (e.g., Ubuntu, Fedora)"),
      ("Kernel", "Core component of the OS that manages hardware, memory, and processes"),
      ("Debian", "Distribution family using dpkg/.deb packages. Known for stability."),
      ("Ubuntu", "Debian-based distro by Mark Shuttleworth (2004). Releases every 6 months, LTS every 2 years."),
      ("Red Hat", "Distribution family using rpm packages. Enterprise-focused."),
      ("RHEL", "Red Hat Enterprise Linux. Commercial, subscription-based, optimized for servers."),
      ("CentOS", "Free rebuild of RHEL without commercial support. Server-optimized."),
      ("Fedora", "Community distro sponsored by Red Hat. Cutting-edge, adopts new tech quickly."),
      ("openSUSE", "Community distro from SUSE. Tumbleweed=rolling, Leap=stable."),
      ("LTS", "Long Term Support. Ubuntu LTS supported for 5 years, released every 2 years (even years)."),
      ("Rolling Release", "Distro model with continuous updates, no major version upgrades (e.g., Arch, KALI, Tumbleweed)"),
      ("Android", "Mobile OS based on the Linux kernel, developed by Google"),
      ("Raspberry Pi", "Small single-board computer. OS stored on microSD card. Runs Raspbian/Raspberry Pi OS."),
      ("Embedded Systems", "Devices running Linux with a specific purpose (routers, smart TVs, IoT devices)"),
      ("Cloud Computing", "On-demand delivery of computing resources over the internet (AWS, Azure, GCP)"),
    ],
    "commands": []
  },
  "1.2": {
    "concepts": [
      ("dpkg", "Low-level Debian package manager. Installs .deb files directly."),
      ("apt / apt-get", "High-level Debian package manager. Handles dependencies automatically."),
      ("rpm", "Low-level Red Hat package manager. Installs .rpm files."),
      ("yum / dnf", "High-level Red Hat package managers. dnf is the modern replacement for yum."),
      ("zypper", "Package manager for SUSE/openSUSE distributions"),
      ("GIMP", "GNU Image Manipulation Program. Raster/bitmap image editor."),
      ("Inkscape", "Vector graphics editor for SVG files"),
      ("Blender", "3D modeling, animation, and rendering application"),
      ("Audacity", "Audio editing application"),
      ("LibreOffice", "Open-source office suite (Writer, Calc, Impress, Draw)"),
      ("Apache httpd", "Most widely deployed open-source web server"),
      ("NGINX", "Web server/reverse proxy known for high performance and concurrency"),
      ("Samba", "File sharing between Linux and Windows machines on a network"),
      ("Chromium", "Open-source web browser that Google Chrome is based on"),
      ("MySQL / MariaDB", "Open-source relational database management systems"),
    ],
    "commands": [
      ("apt-get install blender", "Install the Blender package on Debian/Ubuntu"),
      ("apt-cache search figlet", "Search for a package named figlet in Debian repositories"),
      ("yum search cowsay", "Search for a package in Red Hat repositories"),
      ("sudo apt-get remove figlet", "Remove an installed package on Debian/Ubuntu"),
    ]
  },
  "1.3": {
    "concepts": [
      ("FLOSS", "Free/Libre Open Source Software"),
      ("Copyleft", "License type requiring derivatives to keep the same license (e.g., GNU GPL)"),
      ("Permissive License", "License allowing derivatives to use any license (e.g., MIT, BSD, Apache)"),
      ("GNU GPL", "Copyleft license. 4 freedoms: run, study/modify, redistribute, distribute modified versions."),
      ("BSD License", "Permissive license. Minimal restrictions on reuse."),
      ("MIT License", "Permissive license. Very short and simple, allows almost any use."),
      ("Apache License", "Permissive license with patent protection clause"),
      ("Creative Commons", "Licensing framework for creative works, gives authors control over rights"),
      ("Open Source", "'Free as in freedom, not free as in beer' — refers to liberty to use/modify/share, not zero cost"),
      ("FSF", "Free Software Foundation, founded by Richard Stallman"),
      ("Tivoization", "Using hardware restrictions to prevent users from running modified software"),
    ],
    "commands": []
  },
  "1.4": {
    "concepts": [
      ("Desktop Environment", "GUI layer (GNOME, KDE, XFCE) providing windows, menus, icons"),
      ("Terminal Emulator", "Application providing command-line access within a GUI"),
      ("Virtual Console", "Text-based login accessed with Ctrl+Alt+F1-F6"),
      ("HTTPS", "HTTP over TLS/SSL. Encrypts web traffic. Uses port 443."),
      ("TLS/SSL", "Encryption protocols securing network communication"),
      ("SSH", "Secure Shell. Encrypted remote login/command execution. Port 22."),
      ("Password Manager", "Application storing credentials in an encrypted vault"),
    ],
    "commands": []
  },
  "2.1": {
    "concepts": [
      ("Shell", "Command-line interpreter. Reads commands and executes them."),
      ("Bash", "Bourne Again Shell. Most common Linux shell."),
      ("Command", "Program name typed at the prompt (e.g., ls, cd, cat)"),
      ("Option/Flag", "Modifies command behavior. Starts with - or -- (e.g., -l, --all)"),
      ("Argument", "Data passed to a command (e.g., filename, directory path)"),
      ("Environment Variable", "Named value available to all child processes (set with export)"),
      ("Local Variable", "Variable available only in current shell session"),
      ("$PATH", "Environment variable listing directories searched for commands"),
      ("Quoting (double)", "Double quotes: variables ARE expanded. echo \"$HOME\" shows /home/user"),
      ("Quoting (single)", "Single quotes: variables NOT expanded. echo '$HOME' shows literal $HOME"),
      ("Shell Builtin", "Command built into the shell itself (cd, echo, exit, export, type)"),
      ("External Command", "Separate executable file (ls, cat, grep). Found via $PATH."),
    ],
    "commands": [
      ("echo $HOME", "Display the value of the HOME environment variable"),
      ("type cd", "Show that cd is a shell builtin"),
      ("type ls", "Show that ls is an external command (/usr/bin/ls)"),
      ("export VAR=value", "Create an environment variable available to child processes"),
      ("unset VAR", "Remove/delete a variable"),
      ("which nano", "Show the full path of a command's executable"),
      ("echo $PATH", "Display the directories searched for commands"),
      ("PATH=$PATH:/new/dir", "Add a directory to the PATH variable"),
      ("env", "Display all environment variables"),
    ]
  },
  "2.2": {
    "concepts": [
      ("man", "Manual pages. Organized in sections (1=commands, 5=config files, 8=admin)"),
      ("info", "GNU documentation system. Pages are called 'nodes'."),
      ("/usr/share/doc/", "Directory containing documentation for installed packages"),
      ("--help", "Option most commands accept to show brief usage information"),
      ("apropos", "Search man page descriptions for a keyword (same as man -k)"),
    ],
    "commands": [
      ("man ls", "View the manual page for the ls command"),
      ("man -k copy", "Search for man pages related to 'copy' (same as apropos)"),
      ("info mkdir", "View info documentation for mkdir"),
      ("ls /usr/share/doc/", "List documentation directories for installed packages"),
    ]
  },
  "2.3": {
    "concepts": [
      ("/ (root)", "Top of the filesystem hierarchy. All paths start here."),
      (". (dot)", "Current directory"),
      (".. (double dot)", "Parent directory"),
      ("~ (tilde)", "Current user's home directory"),
      ("Absolute Path", "Full path from root: /home/user/file. Works from anywhere."),
      ("Relative Path", "Path from current directory: ../user/file. Depends on pwd."),
      ("Hidden Files", "Files starting with a dot (.). Shown with ls -a."),
      ("FHS", "Filesystem Hierarchy Standard. Defines directory structure for Linux."),
      ("/home", "Contains user home directories"),
      ("/etc", "System configuration files"),
      ("/var", "Variable data (logs, mail, spool)"),
      ("/tmp", "Temporary files. World-writable with sticky bit."),
      ("/usr", "User programs and data (bin, lib, share)"),
      ("/bin, /sbin", "Essential system binaries (/sbin for admin commands)"),
      ("/boot", "Boot loader files and kernel"),
      ("/dev", "Device files (disks, terminals, null)"),
      ("/proc", "Virtual filesystem with process and kernel info"),
      ("/sys", "Virtual filesystem with hardware/driver info"),
    ],
    "commands": [
      ("pwd", "Print working (current) directory"),
      ("cd /etc", "Change directory to /etc (absolute path)"),
      ("cd ..", "Move up one directory (to parent)"),
      ("cd ~", "Go to home directory (same as just cd)"),
      ("ls", "List directory contents"),
      ("ls -l", "Long listing (permissions, owner, size, date)"),
      ("ls -a", "Show all files including hidden (dot files)"),
      ("ls -la", "Long listing including hidden files"),
      ("ls -lrt", "Long listing sorted by time, newest last"),
      ("ls -R", "List directories recursively"),
    ]
  },
  "2.4": {
    "concepts": [
      ("Globbing", "Filename expansion using wildcards: * (any chars), ? (one char), [] (range)"),
      ("Hard Link", "Additional name pointing to the same inode. Cannot cross filesystems."),
      ("Symbolic Link", "Pointer to another filename. Can cross filesystems. Created with ln -s."),
    ],
    "commands": [
      ("touch newfile", "Create an empty file (or update timestamp)"),
      ("mkdir dirname", "Create a directory"),
      ("rmdir dirname", "Remove an empty directory"),
      ("cp src dst", "Copy a file"),
      ("cp -r dir1 dir2", "Copy a directory recursively"),
      ("mv old new", "Move or rename a file/directory"),
      ("rm file", "Remove a file"),
      ("rm -r dir", "Remove a directory and its contents recursively"),
      ("rm -rf dir", "Force remove without prompting"),
      ("ln -s target linkname", "Create a symbolic (soft) link"),
      ("touch \"my file\"", "Create a file with spaces in the name (must quote)"),
    ]
  },
  "3.1": {
    "concepts": [
      ("tar", "Archive utility. Bundles files together. Does NOT compress by default."),
      ("gzip (.gz)", "Compression tool. Fast, moderate compression. Level 1-9 (default 6)."),
      ("bzip2 (.bz2)", "Compression tool. Slower than gzip, better compression."),
      ("xz (.xz)", "Compression tool. Slowest, best compression ratio."),
      ("zip", "Archive AND compress in one step (unlike tar). Common for Windows interop."),
      ("tar -z flag", "Use gzip compression (.tar.gz)"),
      ("tar -j flag", "Use bzip2 compression (.tar.bz2)"),
      ("tar -J flag", "Use xz compression (.tar.xz)"),
      ("tar -f flag", "Specify archive filename. Must be last flag before filename."),
    ],
    "commands": [
      ("tar cf archive.tar files", "Create a tar archive (no compression)"),
      ("tar czf archive.tar.gz files", "Create gzip-compressed tar archive"),
      ("tar cjf archive.tar.bz2 files", "Create bzip2-compressed tar archive"),
      ("tar cJf archive.tar.xz files", "Create xz-compressed tar archive"),
      ("tar tf archive.tar", "List contents of archive without extracting"),
      ("tar xzf archive.tar.gz", "Extract a gzip-compressed tar archive"),
      ("gzip file", "Compress file with gzip (replaces original)"),
      ("gunzip file.gz", "Decompress a gzip file"),
      ("zip -r archive.zip dir/", "Create zip archive of directory (-r for recursive)"),
      ("unzip archive.zip", "Extract a zip archive"),
      ("gzip -9 file", "Compress with maximum compression (slowest)"),
      ("gzip -1 file", "Compress with minimum compression (fastest)"),
    ]
  },
  "3.2": {
    "concepts": [
      ("STDIN (fd 0)", "Standard input. Default: keyboard."),
      ("STDOUT (fd 1)", "Standard output. Default: terminal screen."),
      ("STDERR (fd 2)", "Standard error. Default: terminal screen. Separate from STDOUT."),
      ("> (redirect)", "Redirect STDOUT to file (overwrites)"),
      (">> (append)", "Append STDOUT to file"),
      ("2>", "Redirect STDERR to file"),
      ("&>", "Redirect both STDOUT and STDERR to file"),
      ("< (input)", "Redirect file as STDIN to command"),
      ("| (pipe)", "Send STDOUT of one command as STDIN to another"),
      ("Regular Expression", "Pattern matching syntax used by grep, sed, awk"),
    ],
    "commands": [
      ("grep pattern file", "Search for lines matching pattern in file"),
      ("grep -i pattern file", "Case-insensitive search"),
      ("grep -r pattern dir/", "Recursive search through directories"),
      ("grep -n pattern file", "Show line numbers with matches"),
      ("cat file", "Display entire file contents"),
      ("head -n 5 file", "Show first 5 lines of file"),
      ("tail -n 5 file", "Show last 5 lines of file"),
      ("tail -f logfile", "Follow/watch a log file in real-time"),
      ("wc -l file", "Count number of lines in file"),
      ("sort file", "Sort lines alphabetically"),
      ("sort -n file", "Sort lines numerically"),
      ("cut -d: -f1 /etc/passwd", "Extract field 1 using : as delimiter"),
      ("find /etc -name \"*.conf\"", "Find files by name pattern"),
      ("locate README", "Fast file search using index database"),
      ("sudo updatedb", "Update the locate database"),
      ("cat /etc/* > out 2> /dev/null", "Concatenate files, discard errors"),
    ]
  },
  "3.3": {
    "concepts": [
      ("Shebang (#!)", "First line of script specifying interpreter: #!/bin/bash"),
      ("Execute Permission", "Script needs chmod +x to run directly"),
      ("$1, $2, ...", "Positional parameters (script arguments)"),
      ("$#", "Number of arguments passed to script"),
      ("$?", "Exit status of last command (0=success, non-zero=error)"),
      ("if/then/fi", "Conditional execution in bash"),
      ("for/do/done", "Loop construct in bash"),
      ("Variable Assignment", "No spaces around =. VAR=value (not VAR = value)"),
      ("Command Substitution", "$(command) — captures output of a command into a variable"),
    ],
    "commands": [
      ("#!/bin/bash", "Shebang line — tells system to use bash interpreter"),
      ("chmod +x script.sh", "Make a script executable"),
      ("./script.sh", "Run a script in current directory"),
      ("echo $?", "Show exit status of last command"),
      ("echo $#", "Show number of script arguments"),
      ("read VAR", "Read user input into a variable"),
      ("export VAR=value", "Make variable available to child processes"),
      ("bash -c 'command'", "Run a command in a new bash subprocess"),
    ]
  },
  "4.1": {
    "concepts": [
      ("Operating System", "Software managing hardware resources and providing services to applications"),
      ("Windows", "Microsoft proprietary OS. Dominant on desktops. Uses NTFS filesystem."),
      ("macOS", "Apple proprietary OS based on Unix (Darwin kernel). Uses APFS."),
      ("Linux", "Open-source OS. Dominant on servers, embedded, supercomputers."),
      ("Dual Boot", "Installing two OSes on one machine, choosing at startup via bootloader"),
      ("Virtual Machine", "Software-emulated computer running inside another OS (VirtualBox, VMware)"),
    ],
    "commands": [
      ("uname -r", "Display kernel version"),
      ("uname -a", "Display all system information"),
    ]
  },
  "4.2": {
    "concepts": [
      ("CPU", "Central Processing Unit. Executes instructions."),
      ("RAM", "Random Access Memory. Volatile, fast, temporary storage."),
      ("Motherboard", "Main circuit board connecting all components"),
      ("SATA", "Serial ATA. Most common bus for consumer hard drives/SSDs."),
      ("NVMe", "Non-Volatile Memory Express. Fastest storage, connects via PCIe."),
      ("SAS", "Serial Attached SCSI. Enterprise/server drive interface."),
      ("SSD", "Solid State Drive. No moving parts, faster than HDD."),
      ("HDD", "Hard Disk Drive. Magnetic spinning platters. Cheaper per GB."),
      ("Partition", "Logical division of a physical disk"),
      ("GPU", "Graphics Processing Unit. Handles display rendering."),
      ("Power Supply", "Converts AC wall power to DC for computer components"),
      ("Peripheral", "External device (keyboard, mouse, printer, USB drive)"),
      ("Driver", "Software enabling OS to communicate with hardware devices"),
      ("/dev/sda", "First SATA/SCSI disk. sdb=second, sda1=first partition."),
    ],
    "commands": [
      ("lscpu", "Display CPU architecture information"),
      ("free -h", "Display memory usage in human-readable format"),
      ("lsblk", "List block devices (disks and partitions)"),
      ("lsblk -f", "List block devices with filesystem info"),
    ]
  },
  "4.3": {
    "concepts": [
      ("Process", "Running instance of a program"),
      ("PID", "Process ID. Unique number identifying each running process."),
      ("Daemon", "Background process providing a service (e.g., sshd, httpd)"),
      ("init/systemd", "First process started (PID 1). Parent of all other processes."),
      ("/var/log/", "Directory containing system log files"),
      ("/proc/cpuinfo", "Virtual file showing CPU information"),
      ("/proc/cmdline", "Kernel boot parameters"),
      ("Package Repository", "Server hosting software packages for download/install"),
      ("/etc/apt/sources.list", "Debian/Ubuntu repository configuration file"),
    ],
    "commands": [
      ("ps", "Show running processes for current user"),
      ("ps aux", "Show all running processes with details"),
      ("top", "Interactive process viewer (M=memory, P=CPU, N=PID sort)"),
      ("pstree", "Show processes as parent-child tree"),
      ("kill PID", "Send signal to terminate a process"),
      ("uptime", "Show how long system has been running + load averages"),
      ("free -h", "Show RAM and swap usage"),
      ("dmesg", "Display kernel ring buffer messages"),
      ("journalctl", "Query systemd journal (logs)"),
      ("journalctl -k", "Show kernel messages (like dmesg)"),
      ("tail -f /var/log/messages", "Watch log file in real-time"),
      ("last", "Show recent user logins"),
      ("cat /proc/cpuinfo", "Display CPU details"),
    ]
  },
  "4.4": {
    "concepts": [
      ("IP Address", "Unique numeric address for a device on a network"),
      ("IPv4", "32-bit address (e.g., 192.168.1.1). 4 octets in dotted decimal."),
      ("IPv6", "128-bit address (e.g., fe80::1). Written in hexadecimal with colons."),
      ("Subnet Mask", "Defines network vs host portion of IP (e.g., 255.255.255.0 = /24)"),
      ("Gateway", "Router connecting local network to other networks/internet"),
      ("DNS", "Domain Name System. Translates domain names to IP addresses."),
      ("/etc/resolv.conf", "File configuring DNS nameservers on Linux"),
      ("A Record", "DNS record mapping hostname to IPv4 address"),
      ("AAAA Record", "DNS record mapping hostname to IPv6 address"),
      ("MX Record", "DNS record specifying mail server for a domain"),
      ("CNAME", "DNS alias record pointing one name to another"),
      ("TCP", "Transmission Control Protocol. Reliable, connection-oriented."),
      ("UDP", "User Datagram Protocol. Fast, connectionless, no guaranteed delivery."),
      ("Port", "Number identifying a network service (22=SSH, 80=HTTP, 443=HTTPS)"),
      ("Socket", "Combination of IP address + port number"),
      ("MAC Address", "Hardware address of a network interface (48-bit, e.g., aa:bb:cc:dd:ee:ff)"),
    ],
    "commands": [
      ("ip addr show", "Display network interface addresses"),
      ("ip route show", "Display routing table"),
      ("ping -c 3 8.8.8.8", "Test connectivity with 3 ICMP packets"),
      ("host example.com", "DNS lookup for a domain"),
      ("dig example.com", "Detailed DNS query"),
      ("ss -t", "Show active TCP connections"),
      ("cat /etc/resolv.conf", "View DNS configuration"),
    ]
  },
  "5.1": {
    "concepts": [
      ("root", "Superuser account with UID 0. Full system access."),
      ("UID 0", "User ID of the root (superuser) account"),
      ("UID 1000", "Typical UID of the first standard user account"),
      ("/etc/passwd", "User account info file. Readable by all. Fields: user:x:UID:GID:comment:home:shell"),
      ("/etc/shadow", "Encrypted password file. Readable only by root. !! means account locked."),
      ("/etc/group", "Group information file. Lists groups and their members."),
      ("SUID bit", "Set User ID. File executes with owner's permissions. Why normal users can run passwd."),
      ("# vs $", "# = root prompt. $ = normal user prompt."),
      ("/ vs /root", "/ = filesystem root directory. /root = root user's home directory."),
      ("su -", "Switch to root user with root's environment"),
      ("sudo", "Execute a single command with root privileges"),
    ],
    "commands": [
      ("whoami", "Display current username"),
      ("id", "Show UID, GID, and group memberships"),
      ("who", "List currently logged-in users"),
      ("w", "Show who is logged in and what they're doing"),
      ("last", "Show recent login history"),
      ("sudo command", "Run a command as root"),
      ("su -", "Switch to root user"),
      ("cat /etc/passwd", "View user account information"),
      ("cat /etc/shadow", "View encrypted passwords (root only)"),
    ]
  },
  "5.2": {
    "concepts": [
      ("useradd", "Create a new user account"),
      ("usermod", "Modify an existing user account"),
      ("userdel", "Delete a user account"),
      ("groupadd", "Create a new group"),
      ("passwd", "Set or change a user's password"),
      ("/etc/skel/", "Skeleton directory. Files here are copied to new user's home directory."),
    ],
    "commands": [
      ("useradd -m newuser", "Create user with home directory"),
      ("useradd -M newuser", "Create user WITHOUT home directory"),
      ("passwd newuser", "Set password for newuser"),
      ("groupadd devs", "Create a new group called devs"),
      ("usermod -aG sudo user", "Add user to sudo group (-a=append, -G=group)"),
      ("chsh -s /bin/zsh", "Change login shell to zsh"),
      ("id newuser", "Show UID/GID/groups for newuser"),
    ]
  },
  "5.3": {
    "concepts": [
      ("Permission Types", "r=read(4), w=write(2), x=execute(1)"),
      ("Permission Classes", "u=user/owner, g=group, o=others, a=all"),
      ("Octal Permissions", "Three digits: owner-group-others. e.g., 755 = rwxr-xr-x"),
      ("umask", "Default permission mask. Subtracted from 666(files)/777(dirs). umask 022 → files=644, dirs=755"),
      ("Sticky Bit", "Set on /tmp. Prevents users from deleting files they don't own. Shown as 't'."),
      ("SUID", "Set User ID bit. File runs as file owner. Shown as 's' in owner execute position."),
      ("SGID", "Set Group ID bit. File runs as file's group. On dir: new files inherit group."),
      ("chown", "Change file owner (and optionally group)"),
      ("chgrp", "Change file group only"),
      ("chmod", "Change file permissions"),
    ],
    "commands": [
      ("chmod 755 file", "Set rwxr-xr-x (owner full, group+others read+execute)"),
      ("chmod 644 file", "Set rw-r--r-- (owner read+write, others read only)"),
      ("chmod u+x file", "Add execute permission for owner"),
      ("chmod go-w file", "Remove write permission from group and others"),
      ("chmod +t /dir", "Set sticky bit on directory"),
      ("chown user:group file", "Change owner and group"),
      ("chown -R user dir/", "Change owner recursively"),
      ("umask", "Display current umask value"),
      ("umask 022", "Set umask (new files get 644, dirs get 755)"),
      ("ls -l file", "View permissions, owner, group, size, date"),
      ("stat file", "Detailed file info including permissions in octal"),
    ]
  },
  "5.4": {
    "concepts": [
      ("Symbolic Link", "Pointer to another file path. Can cross filesystems. Created with ln -s."),
      ("Hard Link", "Additional directory entry pointing to same inode. Cannot cross filesystems."),
      ("Inode", "Data structure storing file metadata (permissions, owner, timestamps, block locations)"),
      ("/tmp", "World-writable temp directory. Sticky bit prevents others deleting your files. Cleared on reboot."),
      ("/var/tmp", "Temporary files that persist across reboots"),
      (".hidden files", "Files/dirs starting with dot. Not shown by default. Use ls -a to see."),
      (".bashrc", "Bash configuration file run for each interactive non-login shell"),
      (".profile", "Profile file run at login. Sets up environment."),
    ],
    "commands": [
      ("ln -s target link", "Create symbolic link"),
      ("ln target link", "Create hard link"),
      ("ls -la", "List all files including hidden, in long format"),
      ("ls -d */", "List only directories"),
      ("file myfile", "Determine file type by contents (not extension)"),
      ("stat myfile", "Show detailed file metadata (inode, permissions, timestamps)"),
    ]
  },
}

# Replace concepts and commands in structured data
for sec_id, cards in CLEAN.items():
    if sec_id not in data:
        continue
    # Replace concepts
    data[sec_id]['concepts'] = [{'term': t, 'definition': d} for t, d in cards['concepts']]
    # Replace commands
    data[sec_id]['commands'] = [{'command': c, 'context': d} for c, d in cards['commands']]

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

total_concepts = sum(len(c['concepts']) for c in CLEAN.values())
total_commands = sum(len(c['commands']) for c in CLEAN.values())
print(f"Replaced all cards with {total_concepts} clean concepts + {total_commands} clean commands = {total_concepts+total_commands} total")
