"""Add Quizlet flashcards from visible preview content."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cards visible from Quizlet previews
QUIZLET_CARDS = [
    # From Topic 5 set
    {"section":"5.1","term":"UID","def":"User Identifier, an enumerated reference to a user account"},
    {"section":"5.1","term":"GID","def":"Group Identifier, an enumerated reference to a group account"},
    {"section":"5.1","term":"Primary GID","def":"The default group a user has"},
    {"section":"5.1","term":"Superuser","def":"Another name for the root user. Has a UID of 0"},
    {"section":"5.1","term":"Standard User Accounts","def":"Can't change system settings and can store files in their designated area only"},
    {"section":"5.1","term":"System Accounts","def":"Organized way of naming and categorizing accounts with no defined shell and limited or no privileges"},
    {"section":"5.1","term":"Service Accounts","def":"Accounts used to provide privileged access used by system services and core applications"},
    {"section":"5.1","term":"Login shell","def":"The shell that is opened directly after a user has logged in"},
    {"section":"5.1","term":"chsh","def":"Changes the login shell"},
    {"section":"5.1","term":"id","def":"List the current information of a user (UID, GID, groups)"},
    {"section":"5.1","term":"last","def":"Listing the last time users have logged into the system"},
    {"section":"5.1","term":"who","def":"Lists active logins on a system"},
    {"section":"5.1","term":"su","def":"Switch user. Most commonly used as 'su -' which switches to root"},
    {"section":"5.1","term":"sudo","def":"Run a single command as root (superuser do)"},
    {"section":"5.1","term":"/etc/passwd","def":"Stores basic information about users on the system, including UID, GID, home directory, shell, etc. (no actual passwords)"},
    {"section":"5.1","term":"/etc/passwd format","def":"USERNAME:PASSWORD:UID:GID:GECOS:HOMEDIR:SHELL — Password field is generally 'x', meaning password is stored in /etc/shadow"},
    
    # From Complete set - Topic 1 cards visible
    {"section":"1.1","term":"LPI","def":"Linux Professional Institute"},
    {"section":"1.1","term":"Linux","def":"An open-source operating system inspired by Unix. One of the most popular operating systems available today."},
    {"section":"1.1","term":"Linus Torvalds","def":"Finnish graduate student who developed Linux starting in 1991 and distributed it under the GNU Public License."},
    {"section":"1.1","term":"Unix","def":"Operating system developed by AT&T in the 1970s. Considered portable, meaning it can run on just about any hardware platform."},
    {"section":"1.1","term":"Linux Distribution","def":"Bundles of software that contain the Linux kernel, utilities and a graphical desktop; also called distros."},
    {"section":"1.1","term":"Debian","def":"A distribution family that uses the package manager dpkg and the package format .deb"},
    {"section":"1.1","term":"dpkg","def":"Package manager used by Debian GNU/Linux, Ubuntu, and other Debian derivatives"},
    {"section":"1.1","term":"Ubuntu","def":"A Debian-based distribution created by Mark Shuttleworth in 2004. Releases every 6 months, LTS every 2 years."},
    {"section":"1.1","term":"Red Hat","def":"A Linux distribution family that uses Red Hat Package Manager (RPM). Specializes in open source software."},
    {"section":"1.1","term":"rpm","def":"Red Hat Package Manager — package format used by Red Hat family distros"},
    {"section":"1.1","term":"RHEL","def":"Red Hat Enterprise Linux: reliable enterprise solution with subscriptions/licenses. Optimized for servers."},
    {"section":"1.1","term":"CentOS","def":"A project that compiles RHEL into a free distribution without commercial support. Optimized for servers."},
    {"section":"1.1","term":"Fedora","def":"Community-supported distribution sponsored by Red Hat. Progressive, adopts new tech quickly. Free."},
]

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

added = 0
for card in QUIZLET_CARDS:
    sec_id = card['section']
    if sec_id in data:
        # Check for duplicates by term
        existing_terms = [c['term'].lower() for c in data[sec_id]['concepts']]
        if card['term'].lower() not in existing_terms:
            data[sec_id]['concepts'].append({'term': card['term'], 'definition': card['def']})
            added += 1

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added {added} new cards from Quizlet (skipped duplicates)")
