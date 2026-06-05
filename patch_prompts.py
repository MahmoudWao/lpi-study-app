import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix command card fronts - remove the emoji prompt, just show the command
content = content.replace(
    "front:`\U0001f4bb What does this command do?\\n\\n$ ${cmd.command}`",
    "front:`$ ${cmd.command}`"
)
content = content.replace(
    "front:`\u2328\ufe0f What command would you use to:\\n\\n${ctx}`",
    "front:`${ctx}`"
)

# Fix concept card fronts
content = content.replace(
    "front:`\U0001f4dd Define:\\n\\n${c.term}`",
    "front:`${c.term}`"
)
content = content.replace(
    "front:`\U0001f50d What term?\\n\\n${cleanDef.substring(0,150)}`",
    "front:`${cleanDef.substring(0,150)}`"
)

# The challenge mode label already shows card.type, so user knows what kind of card it is.
# Update the focus-label to be more descriptive based on card type
old_label = """<div class="focus-label">${isNew?'\U0001f195 New':'\U0001f504 Review'} \u00b7 ${card.type}</div>"""
new_label = """<div class="focus-label">${isNew?'\U0001f195 New':'\U0001f504 Review'} \u00b7 ${card.type==='command'?'What does this command do?':card.type==='reverse'?'What command does this?':card.type==='concept'?'Define this term':'Answer the question'}</div>"""
content = content.replace(old_label, new_label)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
print("Command front clean:", "What does this command do?" not in content.split("focus-label")[0].split("cards.push")[1])
print("Label updated:", "What does this command do?" in content and "focus-label" in content)
