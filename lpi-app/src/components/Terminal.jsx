import { useState, useRef, useEffect, useCallback } from 'react';
import { TERM_LABS } from '../data/terminal-labs';
import { loadTermProgress, saveTermProgress } from '../utils/storage';
import { esc } from '../utils/helpers';

const VFS_INITIAL = {
  cwd: '/home/student', home: '/home/student', user: 'student',
  files: {
    '/home/student': { type: 'd', children: ['notes.txt', 'script.sh', 'data.txt', 'docs', '.bashrc', '.profile'] },
    '/home/student/docs': { type: 'd', children: ['readme.md', 'report.pdf', 'log.txt'] },
    '/home/student/notes.txt': { type: 'f', perms: '-rw-r--r--', owner: 'student', group: 'student', size: 1024 },
    '/home/student/script.sh': { type: 'f', perms: '-rw-r--r--', owner: 'student', group: 'student', size: 256 },
    '/home/student/data.txt': { type: 'f', perms: '-rw-rw-r--', owner: 'student', group: 'student', size: 4096 },
    '/home/student/.bashrc': { type: 'f', perms: '-rw-r--r--', owner: 'student', group: 'student', size: 3771 },
    '/home/student/.profile': { type: 'f', perms: '-rw-r--r--', owner: 'student', group: 'student', size: 807 },
    '/etc': { type: 'd', children: ['passwd', 'hosts', 'hostname', 'resolv.conf', 'fstab', 'ssh'] },
    '/etc/passwd': { type: 'f', perms: '-rw-r--r--', owner: 'root', group: 'root', size: 2847, content: 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\nsys:x:3:3:sys:/dev:/usr/sbin/nologin\nstudent:x:1000:1000:Student User:/home/student:/bin/bash' },
    '/etc/hosts': { type: 'f', perms: '-rw-r--r--', owner: 'root', group: 'root', size: 221 },
    '/etc/hostname': { type: 'f', perms: '-rw-r--r--', owner: 'root', group: 'root', size: 12, content: 'linux-lab' },
  },
  vars: { NAME: '', HOME: '/home/student', USER: 'student', PATH: '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin', SHELL: '/bin/bash' }
};

function resolvePath(vfs, p) {
  if (!p) return vfs.cwd;
  if (p.startsWith('~')) p = vfs.home + p.slice(1);
  if (p.startsWith('/')) return p.replace(/\/+$/, '') || '/';
  const parts = (vfs.cwd + '/' + p).split('/').filter(Boolean);
  const stack = [];
  parts.forEach(x => { if (x === '..') stack.pop(); else if (x !== '.') stack.push(x); });
  return '/' + stack.join('/');
}

function simulateCommand(vfs, cmd) {
  const parts = cmd.split(/\s+/), base = parts[0];
  switch (base) {
    case 'pwd': return vfs.cwd;
    case 'whoami': return vfs.user;
    case 'hostname': return 'linux-lab';
    case 'id': return parts[1] === '-un' ? vfs.user : parts[1] === '-Gn' ? 'student sudo users' : 'uid=1000(student) gid=1000(student) groups=1000(student),27(sudo)';
    case 'who': return 'student  pts/0  2026-06-05 10:00';
    case 'w': return ' 14:00 up 2 days, 1 user\nUSER  TTY   FROM  LOGIN@  WHAT\nstudent pts/0 :0    10:00   bash';
    case 'users': return 'student';
    case 'groups': return 'student sudo users';
    case 'date': return new Date().toString();
    case 'uname': return parts.includes('-a') ? 'Linux linux-lab 5.15.0 x86_64 GNU/Linux' : 'Linux';
    case 'echo': { let t = parts.slice(1).join(' ').replace(/^["']|["']$/g, ''); t = t.replace(/\$\{?(\w+)\}?/g, (_, v) => vfs.vars[v] || ''); return t; }
    case 'cat': { const p = resolvePath(vfs, parts[1]), f = vfs.files[p]; if (!f) return `cat: ${parts[1]}: No such file or directory`; if (f.type === 'd') return `cat: ${parts[1]}: Is a directory`; return f.content || `[contents of ${parts[1]}]`; }
    case 'ls': { let target = vfs.cwd, showAll = false, showLong = false; for (let i = 1; i < parts.length; i++) { if (parts[i].startsWith('-')) { if (parts[i].includes('a')) showAll = true; if (parts[i].includes('l')) showLong = true; } else target = resolvePath(vfs, parts[i]); } const dir = vfs.files[target]; if (!dir) return `ls: cannot access '${parts[parts.length - 1]}': No such file or directory`; if (dir.type === 'f') { return showLong ? `${dir.perms} 1 ${dir.owner} ${dir.group} ${dir.size} Jun 5 10:00 ${target.split('/').pop()}` : target.split('/').pop(); } let items = dir.children || []; if (showAll) items = ['.', '..', ...items]; if (showLong) return items.map(n => { if (n === '.' || n === '..') return `drwxr-xr-x 2 student student 4096 Jun 5 10:00 ${n}`; const fp = target + '/' + n, f = vfs.files[fp]; return f ? `${f.perms} 1 ${f.owner} ${f.group} ${f.size || 4096} Jun 5 10:00 ${n}` : `drwxr-xr-x 2 student student 4096 Jun 5 10:00 ${n}`; }).join('\n'); return items.join('  '); }
    case 'cd': { const t = parts[1] || vfs.home; vfs.cwd = resolvePath(vfs, t === '~' ? vfs.home : t); return null; }
    case 'mkdir': { const n = parts[parts.length - 1], p = resolvePath(vfs, n); vfs.files[p] = { type: 'd', children: [] }; const par = vfs.cwd; if (vfs.files[par] && vfs.files[par].children) vfs.files[par].children.push(n); return null; }
    case 'touch': { const n = parts[1], p = resolvePath(vfs, n); vfs.files[p] = { type: 'f', perms: '-rw-r--r--', owner: vfs.user, group: vfs.user, size: 0 }; const par = vfs.cwd; if (vfs.files[par] && vfs.files[par].children && !vfs.files[par].children.includes(n)) vfs.files[par].children.push(n); return null; }
    case 'cp': { const s = parts[1], d = parts[2]; const sp = resolvePath(vfs, s); if (!vfs.files[sp]) return `cp: cannot stat '${s}': No such file or directory`; vfs.files[resolvePath(vfs, d)] = { ...vfs.files[sp] }; return null; }
    case 'mv': { const s = parts[1], d = parts[2]; const sp = resolvePath(vfs, s); if (!vfs.files[sp]) return `mv: cannot stat '${s}': No such file or directory`; vfs.files[resolvePath(vfs, d)] = vfs.files[sp]; delete vfs.files[sp]; return null; }
    case 'rm': { const target2 = parts.filter(p2 => !p2.startsWith('-'))[1]; if (!target2) return 'rm: missing operand'; const p = resolvePath(vfs, target2); if (!vfs.files[p]) return `rm: cannot remove '${target2}': No such file or directory`; delete vfs.files[p]; return null; }
    case 'rmdir': { delete vfs.files[resolvePath(vfs, parts[1])]; return null; }
    case 'chmod': case 'chown': return null;
    case 'grep': { const pat = parts[1]?.replace(/['"]/g, ''), file = parts[2]; if (!file) return 'Usage: grep PATTERN FILE'; const p = resolvePath(vfs, file), f = vfs.files[p]; if (!f) return `grep: ${file}: No such file or directory`; return f.content ? f.content.split('\n').filter(l => l.includes(pat)).join('\n') : `[matches for "${pat}"]`; }
    case 'wc': { const file = parts[parts.length - 1], p = resolvePath(vfs, file), f = vfs.files[p]; if (!f) return `wc: ${file}: No such file or directory`; if (f.content) { const l = f.content.split('\n').length; return parts.includes('-l') ? `${l} ${file}` : `  ${l}  ${f.content.split(/\s+/).length} ${f.content.length} ${file}`; } return parts.includes('-l') ? `5 ${file}` : `  5  25 100 ${file}`; }
    case 'head': { const n = parts.indexOf('-n') > -1 ? parseInt(parts[parts.indexOf('-n') + 1]) : parts[1]?.startsWith('-') ? parseInt(parts[1].slice(1)) : 10; const file = parts[parts.length - 1], p = resolvePath(vfs, file), f = vfs.files[p]; if (!f) return `head: cannot open '${file}'`; return f.content ? f.content.split('\n').slice(0, n).join('\n') : `[first ${n} lines]`; }
    case 'tail': return `[last 10 lines of ${parts[parts.length - 1]}]`;
    case 'find': return '/etc/resolv.conf\n/etc/ssh/sshd_config';
    case 'tar': case 'gzip': case 'gunzip': return null;
    case 'man': return `NAME\n    ${parts[1]} - manual page\n\nSYNOPSIS\n    ${parts[1]} [OPTION]... [FILE]...\n\n(press q to exit)`;
    case 'type': { const builtins = ['cd', 'echo', 'exit', 'export', 'type']; return builtins.includes(parts[1]) ? `${parts[1]} is a shell builtin` : `${parts[1]} is /usr/bin/${parts[1]}`; }
    case 'apropos': return 'cp (1) - copy files and directories';
    case 'help': return 'Commands: ls cd pwd cat cp mv rm mkdir rmdir touch chmod grep find\nwc head tail tar gzip echo man type whoami id groups ping ip\n\nLab: hint, reset, labs, clear';
    case 'ifconfig': return 'eth0: inet 192.168.1.100  netmask 255.255.255.0';
    case 'ip': if (parts[1] === 'addr' || parts[1] === 'a') return '2: eth0: inet 192.168.1.100/24'; if (parts[1] === 'route') return 'default via 192.168.1.1 dev eth0\n192.168.1.0/24 dev eth0'; return 'Usage: ip [addr|route]';
    case 'ping': return 'PING google.com (142.250.80.46)\n64 bytes: icmp_seq=1 ttl=118 time=12ms\n64 bytes: icmp_seq=2 ttl=118 time=11ms\n64 bytes: icmp_seq=3 ttl=118 time=12ms\n--- 3 packets, 0% loss';
    case 'route': return 'default  192.168.1.1  UG  eth0\n192.168.1.0/24  *  U  eth0';
    case 'dig': return `;; ANSWER:\n${parts[1] || 'google.com'}. 300 IN A 142.250.80.46`;
    case 'nslookup': return `Name: ${parts[1] || 'google.com'}\nAddress: 142.250.80.46`;
    case 'host': return `${parts[1] || 'google.com'} has address 142.250.80.46`;
    case 'netstat': return 'tcp 0 0 192.168.1.100:22 0.0.0.0:* LISTEN';
    case 'printenv': return parts[1] ? (vfs.vars[parts[1]] || '') : Object.entries(vfs.vars).map(([k, v]) => `${k}=${v}`).join('\n');
    case 'env': return Object.entries(vfs.vars).map(([k, v]) => `${k}=${v}`).join('\n');
    case 'export': { const m = cmd.match(/export\s+(\w+)=(.*)/); if (m) vfs.vars[m[1]] = m[2].replace(/['"]/g, ''); return null; }
    case 'stat': { const p = resolvePath(vfs, parts[1]), f = vfs.files[p]; return f ? `File: ${parts[1]}\nSize: ${f.size || 4096}\nAccess: ${f.perms || '0644'}\nOwner: ${f.owner || vfs.user}` : `stat: cannot stat '${parts[1]}'`; }
    default: { const vm = cmd.match(/^(\w+)=(.*)$/); if (vm) { vfs.vars[vm[1]] = vm[2].replace(/['"]/g, ''); return null; } if (cmd.includes('|')) return '[pipe output]'; return `bash: ${base}: command not found`; }
  }
}

export default function Terminal() {
  const [currentLab, setCurrentLab] = useState(null);
  const [labProgress, setLabProgress] = useState(loadTermProgress);
  const [output, setOutput] = useState([{ type: 'output', text: 'Welcome! Complete the tasks above using Linux commands.\nType "hint" for help · "reset" to restart · "clear" to clear\n' }]);
  const [history, setHistory] = useState([]);
  const [histIdx, setHistIdx] = useState(-1);
  const vfsRef = useRef(JSON.parse(JSON.stringify(VFS_INITIAL)));
  const inputRef = useRef(null);
  const bodyRef = useRef(null);

  useEffect(() => { if (inputRef.current) inputRef.current.focus(); }, [currentLab, output]);
  useEffect(() => { if (bodyRef.current) bodyRef.current.scrollTop = bodyRef.current.scrollHeight; }, [output]);

  const execCommand = useCallback((input) => {
    const cmd = input.trim();
    if (!cmd) return;
    setHistory(h => [cmd, ...h]);
    setHistIdx(-1);
    const newOutput = [{ type: 'cmd', text: cmd }];
    const vfs = vfsRef.current;

    // Special commands
    if (cmd === 'clear') { setOutput([]); return; }
    if (cmd === 'hint') {
      if (!currentLab) { newOutput.push({ type: 'output', text: 'Start a lab first.' }); }
      else {
        const lab = TERM_LABS.find(l => l.id === currentLab);
        const pr = labProgress[lab.id] || [];
        const next = lab.tasks.findIndex((_, i) => !pr.includes(i));
        newOutput.push({ type: 'output', text: next >= 0 ? `💡 ${lab.tasks[next].hint}` : 'All done!' });
      }
      setOutput(o => [...o, ...newOutput]); return;
    }
    if (cmd === 'reset') {
      if (currentLab) {
        const np = { ...labProgress, [currentLab]: [] };
        setLabProgress(np); saveTermProgress(np);
        newOutput.push({ type: 'output', text: 'Lab reset.' });
      } else { newOutput.push({ type: 'output', text: 'No active lab.' }); }
      setOutput(o => [...o, ...newOutput]); return;
    }
    if (cmd === 'labs') {
      newOutput.push({ type: 'output', text: TERM_LABS.map((l, i) => `${i + 1}. ${l.title} (${(labProgress[l.id] || []).length}/${l.tasks.length})`).join('\n') });
      setOutput(o => [...o, ...newOutput]); return;
    }

    // Check lab tasks
    if (currentLab) {
      const lab = TERM_LABS.find(l => l.id === currentLab);
      const pr = labProgress[lab.id] || [];
      for (let i = 0; i < lab.tasks.length; i++) {
        if (!pr.includes(i) && lab.tasks[i].check(cmd)) {
          const newPr = [...pr, i];
          const np = { ...labProgress, [lab.id]: newPr };
          setLabProgress(np); saveTermProgress(np);
          newOutput.push({ type: 'success', text: `✓ Task completed: ${lab.tasks[i].desc}` });
          if (newPr.length === lab.tasks.length) newOutput.push({ type: 'success', text: '\n🎉 Lab complete! All tasks done.' });
          break;
        }
      }
    }

    const result = simulateCommand(vfs, cmd);
    if (result !== null) newOutput.push({ type: result.startsWith('bash:') ? 'error' : 'output', text: result });
    setOutput(o => [...o, ...newOutput]);
  }, [currentLab, labProgress]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') { execCommand(e.target.value); e.target.value = ''; }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (histIdx < history.length - 1) { const ni = histIdx + 1; setHistIdx(ni); e.target.value = history[ni]; } }
    else if (e.key === 'ArrowDown') { e.preventDefault(); if (histIdx > 0) { const ni = histIdx - 1; setHistIdx(ni); e.target.value = history[ni]; } else { setHistIdx(-1); e.target.value = ''; } }
    else if (e.key === 'Tab') { e.preventDefault(); const cmds = ['ls', 'cd', 'pwd', 'cat', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch', 'chmod', 'grep', 'find', 'wc', 'head', 'tail', 'tar', 'echo', 'man', 'type', 'whoami', 'id', 'groups', 'ping', 'clear', 'hint', 'reset']; const m = cmds.filter(c => c.startsWith(e.target.value)); if (m.length === 1) e.target.value = m[0] + ' '; }
  };

  if (!currentLab) {
    return (
      <>
        <div style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--muted)', fontSize: '0.85rem' }}>Practice Linux commands in a simulated terminal</div>
        <div className="grid">
          {TERM_LABS.map(lab => {
            const done = (labProgress[lab.id] || []).length, total = lab.tasks.length;
            return (
              <div key={lab.id} className="sec-card" onClick={() => { setCurrentLab(lab.id); setOutput([{ type: 'output', text: `Lab: ${lab.title}\nType commands to complete tasks. "hint" for help.\n` }]); vfsRef.current = JSON.parse(JSON.stringify(VFS_INITIAL)); }}>
                <div className="icon" style={{ background: done === total ? 'var(--green-light)' : 'var(--card)' }}>💻</div>
                <div className="info"><h3>{lab.title}</h3><div className="meta">Section {lab.section} · {done}/{total} tasks</div></div>
                <div className={`ring ${done === total ? 'ring-3' : done > 0 ? 'ring-1' : ''}`}>{done === total ? '✓' : done > 0 ? done : '-'}</div>
              </div>
            );
          })}
        </div>
      </>
    );
  }

  const lab = TERM_LABS.find(l => l.id === currentLab);
  const progress = labProgress[lab.id] || [];

  return (
    <>
      <button className="back-btn" onClick={() => setCurrentLab(null)}>← Back to Labs</button>
      <div className="term-tasks">
        <h3>📋 {lab.title}</h3>
        {lab.tasks.map((t, i) => {
          const d = progress.includes(i);
          return <div key={i} className={`term-task ${d ? 'done' : ''}`}><span className={d ? 'check' : 'pending'}>{d ? '✓' : '○'}</span><span>{t.desc}</span></div>;
        })}
      </div>
      <div className="term-wrap">
        <div className="term-bar">
          <div className="term-dot" style={{ background: '#f38ba8' }} />
          <div className="term-dot" style={{ background: '#f9e2af' }} />
          <div className="term-dot" style={{ background: '#a6e3a1' }} />
          <span>student@linux-lab:{vfsRef.current.cwd}</span>
        </div>
        <div className="term-body" ref={bodyRef} onClick={() => inputRef.current?.focus()}>
          {output.map((l, i) => (
            <div key={i} className="term-line">
              {l.type === 'cmd' && <><span className="prompt">$</span> <span>{esc(l.text)}</span></>}
              {l.type === 'error' && <span className="error">{esc(l.text)}</span>}
              {l.type === 'success' && <span style={{ color: '#a6e3a1' }}>{esc(l.text)}</span>}
              {l.type === 'output' && esc(l.text)}
            </div>
          ))}
          <div className="term-input-line">
            <span className="prompt">$</span>{' '}
            <input className="term-input" ref={inputRef} type="text" autoFocus spellCheck="false" autoComplete="off" onKeyDown={handleKeyDown} />
          </div>
        </div>
      </div>
      <p style={{ color: 'var(--muted)', fontSize: '0.73rem', textAlign: 'center', marginTop: '0.5rem' }}>hint · reset · clear</p>
    </>
  );
}
