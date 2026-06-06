"""Patch ebook.html: make TOC entries clickable links that jump to the right page."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\ebook.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add TOC linking in the renderPage function
# Replace the heading detection + rendering with an enhanced version that also handles TOC
old_render = """  // Format: detect headings (ALL CAPS lines, or lines starting with #/numbers like "1.1 ")
  text=text.replace(/^(TOPIC \\d+:.*)/gm,'<h1>$1</h1>');
  text=text.replace(/^(\\d+\\.\\d+\\s+(?:Lesson|Linux|Major|Open|ICT|Command|Using|Creating|Archiving|Searching|Turning|Choosing|Understanding|Where|Your|Basic|Managing|Special).*)/gm,'<h2>$1</h2>');
  text=text.replace(/^(Introduction|Summary|Guided Exercises|Explorational Exercises|Answers to .*)$/gm,'<h3>$1</h3>');"""

new_render = """  // Format TOC entries as clickable links (lines with dots and page numbers)
  text=text.replace(/^(.+?)\\.{3,}\\s*(\\d+)$/gm,(match,title,pageNum)=>{
    const targetPage=parseInt(pageNum)+7; // offset: PDF page numbers vs array index
    return `<a href="#" class="toc-link" data-page="${targetPage}" style="display:flex;justify-content:space-between;padding:0.3rem 0;color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--border)">`+
      `<span>${title.replace(/\\.+$/,'').trim()}</span><span style="color:var(--muted)">${pageNum}</span></a>`;
  });
  // Format headings
  text=text.replace(/^(TOPIC \\d+:.*)/gm,'<h1>$1</h1>');
  text=text.replace(/^(\\d+\\.\\d+\\s+(?:Lesson|Linux|Major|Open|ICT|Command|Using|Creating|Archiving|Searching|Turning|Choosing|Understanding|Where|Your|Basic|Managing|Special).*)/gm,'<h2>$1</h2>');
  text=text.replace(/^(Introduction|Summary|Guided Exercises|Explorational Exercises|Answers to .*)$/gm,'<h3>$1</h3>');"""

html = html.replace(old_render, new_render)

# Add click handler for TOC links after renderPage
old_scroll = "  window.scrollTo(0,0);"
new_scroll = """  window.scrollTo(0,0);
  // Bind TOC links
  document.querySelectorAll('.toc-link').forEach(a=>{a.onclick=(e)=>{e.preventDefault();const p=parseInt(a.dataset.page);if(p>=0&&p<pages.length){currentPage=p;renderPage()}}});"""
html = html.replace(old_scroll, new_scroll)

with open(r'C:\Users\miikharo\lpi-study-app\ebook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("TOC links added to ebook")
