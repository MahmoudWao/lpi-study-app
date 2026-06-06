export const TERM_LABS=[
  {id:'nav',title:'Filesystem Navigation',section:'2.3',tasks:[
    {desc:'Print your current working directory',check:c=>c==='pwd',hint:'pwd'},
    {desc:'List files in the current directory',check:c=>/^ls(\s|$)/.test(c)&&!/\//.test(c),hint:'ls'},
    {desc:'Change to the /etc directory',check:c=>c==='cd /etc'||c==='cd  /etc',hint:'cd /etc'},
    {desc:'List all files including hidden ones',check:c=>/^ls\s+.*-.*a/.test(c)||/^ls\s+-a/.test(c),hint:'ls -a'},
    {desc:'Go back to your home directory',check:c=>c==='cd ~'||c==='cd'||c==='cd $HOME',hint:'cd ~ or just cd'},
  ]},
  {id:'files',title:'Creating & Managing Files',section:'2.4',tasks:[
    {desc:'Create a directory called "practice"',check:c=>/^mkdir\s+practice$/.test(c),hint:'mkdir practice'},
    {desc:'Create an empty file called "notes.txt"',check:c=>/^touch\s+notes\.txt$/.test(c),hint:'touch notes.txt'},
    {desc:'Copy notes.txt to notes_backup.txt',check:c=>/^cp\s+notes\.txt\s+notes_backup\.txt$/.test(c),hint:'cp notes.txt notes_backup.txt'},
    {desc:'Move notes_backup.txt into practice/',check:c=>/^mv\s+notes_backup\.txt\s+practice(\/)?$/.test(c),hint:'mv notes_backup.txt practice/'},
    {desc:'Remove the practice directory',check:c=>/^rm\s+-r(f)?\s+practice$/.test(c),hint:'rm -r practice'},
  ]},
  {id:'perms',title:'File Permissions',section:'5.3',tasks:[
    {desc:'View detailed file permissions',check:c=>/^ls\s+-l/.test(c),hint:'ls -l'},
    {desc:'Make script.sh executable',check:c=>/^chmod\s+(\+x|u\+x|7[0-9]{2})\s+script\.sh$/.test(c),hint:'chmod +x script.sh'},
    {desc:'Set data.txt to read-only (444)',check:c=>/^chmod\s+444\s+data\.txt$/.test(c),hint:'chmod 444 data.txt'},
    {desc:'View owner of /etc/passwd',check:c=>/^ls\s+-l\s+\/etc\/passwd$/.test(c)||/^stat/.test(c),hint:'ls -l /etc/passwd'},
  ]},
  {id:'archive',title:'Archiving & Compression',section:'3.1',tasks:[
    {desc:'Create backup.tar from docs/',check:c=>/^tar\s+.*c.*f\s+backup\.tar\s+docs/.test(c),hint:'tar cf backup.tar docs/'},
    {desc:'List contents of backup.tar',check:c=>/^tar\s+.*t.*f\s+backup\.tar/.test(c),hint:'tar tf backup.tar'},
    {desc:'Compress backup.tar with gzip',check:c=>/^gzip\s+backup\.tar$/.test(c),hint:'gzip backup.tar'},
    {desc:'Extract backup.tar.gz',check:c=>/^tar\s+.*x.*z.*f\s+backup\.tar\.gz/.test(c),hint:'tar xzf backup.tar.gz'},
  ]},
  {id:'search',title:'Searching & Filtering',section:'3.2',tasks:[
    {desc:'Search for "root" in /etc/passwd',check:c=>/^grep\s+.*root.*\s+\/etc\/passwd$/.test(c),hint:'grep root /etc/passwd'},
    {desc:'Count lines in /etc/passwd',check:c=>/^wc\s+-l\s+\/etc\/passwd$/.test(c),hint:'wc -l /etc/passwd'},
    {desc:'Show first 5 lines of /etc/passwd',check:c=>/^head\s+(-n\s*5|-5)\s+\/etc\/passwd$/.test(c),hint:'head -n 5 /etc/passwd'},
    {desc:'Find .conf files in /etc',check:c=>/^find\s+\/etc.*-name.*\.conf/.test(c),hint:'find /etc -name "*.conf"'},
    {desc:'Pipe ls to grep for "log"',check:c=>/^ls.*\|\s*grep\s+.*log/.test(c),hint:'ls | grep log'},
  ]},
  {id:'scripting',title:'Basic Scripting',section:'3.3',tasks:[
    {desc:'Echo "Hello World"',check:c=>/^echo\s+("Hello World"|'Hello World'|Hello World)$/i.test(c),hint:'echo "Hello World"'},
    {desc:'Create variable NAME="Linux"',check:c=>/^NAME=("Linux"|'Linux'|Linux)$/.test(c),hint:'NAME="Linux"'},
    {desc:'Print the NAME variable',check:c=>/^echo\s+\$NAME$/.test(c),hint:'echo $NAME'},
    {desc:'Display the PATH variable',check:c=>/^echo\s+\$PATH$/.test(c)||/^printenv\s+PATH$/.test(c),hint:'echo $PATH'},
  ]},
  {id:'users',title:'Users & Groups',section:'5.1',tasks:[
    {desc:'Display current username',check:c=>c==='whoami',hint:'whoami'},
    {desc:'List your groups',check:c=>c==='groups'||c==='id',hint:'groups'},
    {desc:'View /etc/passwd',check:c=>/^cat\s+\/etc\/passwd$/.test(c),hint:'cat /etc/passwd'},
    {desc:'Check who is logged in',check:c=>c==='who'||c==='w',hint:'who'},
  ]},
  {id:'network',title:'Networking Basics',section:'4.4',tasks:[
    {desc:'Show network interfaces',check:c=>/^(ifconfig|ip\s+a(ddr)?)$/.test(c),hint:'ip addr'},
    {desc:'Ping google.com (3 packets)',check:c=>/^ping\s+-c\s*3\s+google\.com/.test(c),hint:'ping -c 3 google.com'},
    {desc:'Show routing table',check:c=>/^(route|ip\s+route|netstat\s+-r)/.test(c),hint:'ip route'},
    {desc:'DNS lookup for google.com',check:c=>/^(dig|nslookup|host)\s+google\.com$/.test(c),hint:'dig google.com'},
  ]},
  {id:'help',title:'Getting Help',section:'2.2',tasks:[
    {desc:'View man page for ls',check:c=>/^man\s+ls$/.test(c),hint:'man ls'},
    {desc:'Get help for cp',check:c=>/^cp\s+--help$/.test(c),hint:'cp --help'},
    {desc:'Use apropos to find "copy"',check:c=>/^(apropos|man\s+-k)\s+copy$/.test(c),hint:'apropos copy'},
    {desc:'Check type of cd',check:c=>/^type\s+cd$/.test(c),hint:'type cd'},
  ]},
];
