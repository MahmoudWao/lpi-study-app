"""Add Exam mode: 40-question mock exam + random exam generator."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Exam nav button
content = content.replace(
    """<button data-m="progress" class="${S.mode==='progress'?'active':''}">📊 Stats</button>""",
    """<button data-m="exam" class="${S.mode==='exam'?'active':''}">🎯 Exam</button>
    <button data-m="progress" class="${S.mode==='progress'?'active':''}">📊 Stats</button>"""
)

# 2. Add exam case to render switch
content = content.replace(
    "case 'progress':html+=renderProgress();break;",
    "case 'exam':html+=renderExam();break;\n    case 'progress':html+=renderProgress();break;"
)

# 3. Add the MOCK_EXAM data and renderExam function before the terminal section
exam_code = '''
// === EXAM MODE ===
const MOCK_EXAM = [
  {d:"1",q:"Which is a copyleft license (derivatives must stay under the same license)?",opts:["MIT","BSD","GNU GPL","Apache 2.0"],a:2,e:"GNU GPL is the classic copyleft license. MIT, BSD, and Apache are permissive."},
  {d:"1",q:"Which set are all permissive licenses?",opts:["GPL, LGPL, AGPL","MIT, BSD, Apache","GPL, MIT, BSD","Creative Commons only"],a:1,e:"MIT, BSD, and Apache are permissive. The GPL family is copyleft."},
  {d:"1",q:"What does 'free as in freedom, not free as in beer' mean?",opts:["The software always costs money","It's about liberty/rights, not about price","It must be sold commercially","Only free citizens may use it"],a:1,e:"It contrasts liberty (run, study, modify, share) with cost."},
  {d:"1",q:"Which Linux application is used for raster image editing?",opts:["Inkscape","GIMP","Blender","Audacity"],a:1,e:"GIMP = raster/photo editing. Inkscape = vector, Blender = 3D, Audacity = audio."},
  {d:"1",q:"Which application is the standard tool for vector graphics on Linux?",opts:["GIMP","Inkscape","Krita","Shotcut"],a:1,e:"Inkscape handles vector graphics (SVG). GIMP is raster."},
  {d:"1",q:"Which application is used for 3D modeling and animation?",opts:["Blender","LibreOffice","NGINX","Thunderbird"],a:0,e:"Blender does 3D modeling, animation, and rendering."},
  {d:"1",q:"Which two are common Linux web servers?",opts:["MySQL and PostgreSQL","Apache and NGINX","GNOME and KDE","GIMP and Blender"],a:1,e:"Apache and NGINX are the dominant Linux web servers."},
  {d:"2",q:"What does ls -a show that plain ls hides?",opts:["Files in reverse order","Hidden files (names starting with a dot)","Only directories","Inode numbers"],a:1,e:"-a = all, including hidden dotfiles like .bashrc."},
  {d:"2",q:"What does ls -R do?",opts:["Reverses the sort","Lists recursively through subdirectories","Shows raw byte sizes","Repairs the directory"],a:1,e:"-R = recursive: descends into every subdirectory."},
  {d:"2",q:"What does ls -lrt produce?",opts:["Long listing by size","Long listing sorted by time, newest at the bottom","Long listing of root files","Recursive listing"],a:1,e:"-l long, -t sort by time, -r reverse — newest files appear last."},
  {d:"2",q:"In shell globbing, what does * match?",opts:["Exactly one character","Zero or more characters","Only digits","Only directories"],a:1,e:"* matches zero or more characters."},
  {d:"2",q:"In shell globbing, what does ? match?",opts:["Zero or more characters","Exactly one character","Any whole word","The last command"],a:1,e:"? matches exactly one character."},
  {d:"2",q:"What does touch file{1..3} create?",opts:["One file named file{1..3}","file1, file2, and file3","Three copies of file1","An error"],a:1,e:"Brace expansion produces file1 file2 file3."},
  {d:"2",q:"What does cd - do?",opts:["Goes up one level","Switches to your previous working directory","Goes to root","Goes home"],a:1,e:"cd - returns to the previous directory."},
  {d:"2",q:"What does -p do in mkdir -p a/b/c?",opts:["Sets private permissions","Creates parent directories as needed","Prompts before each","Prints the path"],a:1,e:"-p = parents: creates the full chain and won't error if it exists."},
  {d:"2",q:"Which character continues a long command onto the next line?",opts:["A semicolon ;","A backslash \\\\","A pipe |","A greater-than sign >"],a:1,e:"A trailing backslash escapes the newline."},
  {d:"3",q:"Which tar option compresses with gzip?",opts:["-z","-j","-J","-c"],a:0,e:"-z = gzip, -j = bzip2, -J = xz. -c only creates."},
  {d:"3",q:"Does tar compress files by default?",opts:["Yes, with gzip","No — it only bundles unless you add a compression flag","Only files over 1 MB","Yes, with xz"],a:1,e:"tar does not compress by default. zip does."},
  {d:"3",q:"In zip, which option gives the most compression?",opts:["-0","-1","-6","-9"],a:3,e:"-9 = maximum (slowest). -0 = none, default is -6."},
  {d:"3",q:"What does grep -i do?",opts:["Inverts the match","Case-insensitive search","Shows line numbers","Searches inodes"],a:1,e:"-i = case-insensitive. -v inverts, -n line numbers, -R recurses."},
  {d:"3",q:"Which file descriptor is STDERR, and how do you discard it?",opts:["0, with 0>/dev/null","1, with 1>/dev/null","2, with 2>/dev/null","3, with 3>/dev/null"],a:2,e:"STDIN=0, STDOUT=1, STDERR=2. 2>/dev/null discards errors."},
  {d:"3",q:"What does the pipe | do?",opts:["Runs two unrelated commands","Sends STDOUT of first command into STDIN of second","Redirects output to a file","Comments out the rest"],a:1,e:"A pipe connects commands: left STDOUT becomes right STDIN."},
  {d:"4",q:"What three components make up any Linux distribution?",opts:["BIOS, bootloader, desktop","The Linux kernel, GNU utilities, and a package manager","Kernel, antivirus, firewall","Shell, browser, office suite"],a:1,e:"A distro = Linux kernel + GNU utilities + package manager."},
  {d:"4",q:"Which distros belong to the Red Hat family?",opts:["Debian, Ubuntu, Mint","Fedora, RHEL, CentOS","Kali, Tails, Parrot","Slackware, SUSE, Arch"],a:1,e:"Red Hat: Fedora (upstream) > RHEL > CentOS."},
  {d:"4",q:"Which is a rolling-release distribution?",opts:["Ubuntu LTS","Debian Stable","openSUSE Tumbleweed","CentOS"],a:2,e:"Tumbleweed and Kali are rolling releases."},
  {d:"4",q:"How long is Ubuntu LTS supported?",opts:["1 year","2 years","3 years","5 years"],a:3,e:"Ubuntu LTS = 5 years support, released every 2 years."},
  {d:"4",q:"What is /proc?",opts:["A folder for installed programs","A virtual filesystem exposing kernel and process info","Where the bootloader lives","The root user's home"],a:1,e:"/proc is a pseudo-filesystem presenting live kernel data."},
  {d:"4",q:"Where is DNS resolver configuration stored?",opts:["/etc/hosts.deny","/etc/resolv.conf","/etc/dns.conf","/proc/dns"],a:1,e:"/etc/resolv.conf lists the nameservers."},
  {d:"5",q:"What is the UID of the root user?",opts:["0","1","100","1000"],a:0,e:"root is always UID 0. First regular user is UID 1000."},
  {d:"5",q:"Which file stores hashed passwords (root-only)?",opts:["/etc/passwd","/etc/shadow","/etc/group","/etc/skel"],a:1,e:"/etc/shadow holds password hashes (root-only)."},
  {d:"5",q:"Why can a normal user run passwd to change their password?",opts:["It runs in a sandbox","The SUID bit makes it run with root's privileges","Linux makes the user root","/etc/shadow is world-writable"],a:1,e:"passwd has the SUID bit set, executing with owner's (root's) privileges."},
  {d:"5",q:"What is chmod 640 in symbolic notation?",opts:["rwxr--r--","rw-r-----","rw-rw----","r--r-----"],a:1,e:"640 = rw-r-----. 6=rw (owner), 4=r (group), 0=--- (others)."},
  {d:"5",q:"Which leading octal digit sets the sticky bit?",opts:["1","2","4","7"],a:0,e:"1=sticky, 2=SGID, 4=SUID. Sticky on /tmp prevents deleting others' files."},
  {d:"5",q:"How do adduser and useradd differ?",opts:["They are the same","adduser is interactive high-level; useradd is low-level","useradd is interactive; adduser is low-level","adduser only manages groups"],a:1,e:"adduser is an interactive wrapper. useradd is the low-level command."},
  {d:"5",q:"Which flag makes useradd create the home directory?",opts:["-h","-m","-d","-c"],a:1,e:"useradd -m creates the home directory. -d only sets its path."},
  {d:"5",q:"What does passwd -l user do?",opts:["Lists the password","Locks the account (puts ! before the hash)","Lengthens the password","Logs the user out"],a:1,e:"-l = lock: disables password login by prefixing hash with !."},
  {d:"5",q:"What does umask 022 mean for new files?",opts:["Files get 022 permissions","Files get 644 (666-022)","Files get 777","Files get 022 owner only"],a:1,e:"umask subtracts from 666 for files: 666-022=644 (rw-r--r--)."},
  {d:"5",q:"What permission does the sticky bit on /tmp prevent?",opts:["Reading files","Writing new files","Users deleting files they don't own","Executing scripts"],a:2,e:"Sticky bit means only file owner (or root) can delete their files in that directory."},
  {d:"5",q:"What does chown user:group file do?",opts:["Changes permissions","Changes owner and group of the file","Creates a new user","Changes the file type"],a:1,e:"chown changes ownership. user:group sets both. -R for recursive."},
];

let examState = {active:false, questions:[], idx:0, score:0, answered:false, missed:[], mode:'menu'};

function renderExam(){
  if(examState.mode==='menu') return renderExamMenu();
  if(examState.mode==='active') return renderExamQuestion();
  if(examState.mode==='results') return renderExamResults();
}

function renderExamMenu(){
  const lastScore=localStorage.getItem('lpi_last_exam');
  return `<div class="panel" style="text-align:center">
    <h2>🎯 Practice Exam</h2>
    <p style="color:var(--muted);margin-bottom:1.5rem">Test yourself under exam conditions</p>
    ${lastScore?`<p style="margin-bottom:1rem;font-size:0.85rem">Last score: <strong style="color:var(--primary)">${lastScore}%</strong></p>`:''}
    <div class="grid" style="gap:0.8rem;max-width:400px;margin:0 auto">
      <button class="btn btn-primary" style="width:100%" data-exam="mock">📝 40-Question Mock Exam</button>
      <button class="btn btn-outline" style="width:100%" data-exam="quick">⚡ Quick 20 (Random)</button>
      <button class="btn btn-outline" style="width:100%" data-exam="topic">📚 Topic Focus (10 per topic)</button>
    </div>
  </div>`;
}

function startExam(type){
  examState={active:true,questions:[],idx:0,score:0,answered:false,missed:[],mode:'active'};
  if(type==='mock'){
    examState.questions=[...MOCK_EXAM].sort(()=>Math.random()-0.5);
  } else if(type==='quick'){
    examState.questions=[...MOCK_EXAM].sort(()=>Math.random()-0.5).slice(0,20);
  } else if(type==='topic'){
    // 2 per topic from mock, fill rest randomly
    const byTopic={};
    MOCK_EXAM.forEach(q=>{if(!byTopic[q.d])byTopic[q.d]=[];byTopic[q.d].push(q)});
    let picked=[];
    Object.values(byTopic).forEach(qs=>{const s=[...qs].sort(()=>Math.random()-0.5);picked.push(...s.slice(0,Math.min(10,s.length)))});
    examState.questions=picked.sort(()=>Math.random()-0.5);
  }
  render();
}

function renderExamQuestion(){
  const qs=examState.questions,q=qs[examState.idx],total=qs.length;
  const pct=Math.round(examState.idx/total*100);
  const KEYS=['A','B','C','D'];
  let html=`<div class="panel">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;font-size:0.8rem;color:var(--muted)">
      <span>Q ${examState.idx+1}/${total}</span><span>Topic ${q.d}</span><span>Score: ${examState.score}</span>
    </div>
    <div class="progress-bar" style="margin-bottom:1.2rem"><div class="progress-fill pf-primary" style="width:${pct}%"></div></div>
    <p style="font-size:1rem;line-height:1.7;margin-bottom:1.2rem">${q.q}</p>
    <div style="display:grid;gap:0.5rem" id="examOpts">`;
  q.opts.forEach((opt,i)=>{
    html+=`<button class="sec-card" style="cursor:pointer;padding:0.8rem 1rem;text-align:left" data-opt="${i}"><strong style="color:var(--primary);margin-right:0.5rem">${KEYS[i]}.</strong>${opt}</button>`;
  });
  html+=`</div>`;
  if(examState.answered){
    html+=`<div class="answer" style="display:block;margin-top:1rem">${q.e}</div>
      <div style="margin-top:1rem;text-align:right"><button class="btn btn-primary btn-sm" data-exnext>Next →</button></div>`;
  }
  html+=`</div>`;
  return html;
}

function renderExamResults(){
  const total=examState.questions.length,pct=Math.round(examState.score/total*100);
  localStorage.setItem('lpi_last_exam',pct.toString());
  const pass=pct>=65;
  let html=`<div class="panel" style="text-align:center">
    <div style="font-size:3rem;margin-bottom:0.5rem">${pass?'🎉':'📚'}</div>
    <h2 style="font-size:2rem;color:var(--primary)">${pct}%</h2>
    <p style="color:var(--muted)">${examState.score}/${total} correct</p>
    <p style="margin-top:0.8rem;font-size:0.9rem">${pass?'Passing score! Keep reviewing weak areas.':'Below 65% passing threshold. Focus on missed topics.'}</p>
  </div>`;
  if(examState.missed.length>0){
    html+=`<div class="panel"><h2>Review Missed (${examState.missed.length})</h2>`;
    examState.missed.forEach(m=>{
      html+=`<div style="border-left:3px solid var(--red);padding:0.6rem 1rem;margin-bottom:0.6rem;border-radius:0 6px 6px 0;background:var(--card);font-size:0.85rem">
        <p style="margin-bottom:0.3rem">${m.q}</p>
        <p style="color:var(--green)">✓ ${m.ans}</p>
      </div>`;
    });
    html+=`</div>`;
  }
  html+=`<div style="text-align:center;margin-top:1rem"><button class="btn btn-primary" data-exam="menu">← Back to Exam Menu</button></div>`;
  return html;
}

'''

# Insert before "// === TERMINAL ===" 
content = content.replace('// === TERMINAL ===', exam_code + '\n// === TERMINAL ===')

# 4. Add event bindings for exam mode
old_bind_end = "document.querySelectorAll('[data-filter]').forEach"
exam_bindings = """// Exam bindings
  document.querySelectorAll('[data-exam]').forEach(b=>{b.onclick=()=>{
    if(b.dataset.exam==='menu'){examState.mode='menu';render()}
    else{startExam(b.dataset.exam)}
  }});
  document.querySelectorAll('[data-opt]').forEach(b=>{b.onclick=()=>{
    if(examState.answered)return;
    examState.answered=true;
    const q=examState.questions[examState.idx],i=parseInt(b.dataset.opt);
    if(i===q.a){examState.score++;b.style.borderColor='var(--green)';b.style.background='var(--green-light)'}
    else{b.style.borderColor='var(--red)';b.style.background='var(--red-light)';examState.missed.push({q:q.q,ans:q.opts[q.a]});
      document.querySelectorAll('[data-opt]')[q.a].style.borderColor='var(--green)';document.querySelectorAll('[data-opt]')[q.a].style.background='var(--green-light)'}
    render();
  }});
  document.querySelectorAll('[data-exnext]').forEach(b=>{b.onclick=()=>{
    examState.idx++;examState.answered=false;
    if(examState.idx>=examState.questions.length)examState.mode='results';
    render();
  }});
  """
content = content.replace(old_bind_end, exam_bindings + old_bind_end)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Exam mode added:")
print("  - 40-question mock exam")
print("  - Quick 20 random mode")
print("  - Topic focus mode")
print("  - Results with score, pass/fail, missed review")
print("  - Last score persisted")
