"""Patch app_template.html to fix command and concept card quality."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix commands: skip fragments starting with verbs
old_cmd = """      if(!ctx.endsWith('.'))ctx+='.';
      cards.push({id:`${secId}::cmd::${i}`,type:'command',"""

new_cmd = """      if(!ctx.endsWith('.'))ctx+='.';
      if(/^(Is |Are |Was |Were |Has |Have |Had |Can |Will |Does |Did |Creates? |Contains? )/.test(ctx))return;
      if(ctx.length<15)return;
      cards.push({id:`${secId}::cmd::${i}`,type:'command',"""

content = content.replace(old_cmd, new_cmd)

# 2. Fix concepts: skip definitions that are just "_____ are/is..." fragments
old_concept = """      const cleanDef=c.definition.replace(new RegExp(c.term.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'gi'),'_____').substring(0,200);
      cards.push({id:`${secId}::concept::${i}`,"""

new_concept = """      let cleanDef=c.definition.replace(new RegExp(c.term.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'gi'),'_____').substring(0,200);
      if(/^_____\\s*(are|is|was|were|has|have|can|will)/i.test(cleanDef))return;
      if(/^(are|is|was|were)\\s/i.test(cleanDef))return;
      if(cleanDef.replace(/_/g,'').trim().length<20)return;
      cards.push({id:`${secId}::concept::${i}`,"""

content = content.replace(old_concept, new_concept)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
if 'fragments' not in content and 'cleanDef.replace' in content:
    print("Patch applied successfully")
else:
    print("Check needed")
    
print(f"Commands filter: {'if(ctx.length<15)' in content}")
print(f"Concept filter: {'cleanDef.replace(/_/g' in content}")
