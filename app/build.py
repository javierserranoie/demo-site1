from pathlib import Path
import markdown
import json
import os

ZETTEL = Path(os.getenv("PERSONAL_SITE_ZETTEL", "/zettel"))
SITE = Path("/app/site")
SITE.mkdir(parents=True, exist_ok=True)

SECTIONS = {
    "00-fly": "Fleeting",
    "01-literature": "Literature",
    "02-permanent": "Permanent",
    "03-structure": "Structure",
}

posts = []

def convert_markdown(text):
    """Convert markdown to HTML, creating a fresh converter each time."""
    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    return md.convert(text)

# README → home
readme = ZETTEL / "README.md"
if readme.exists():
    try:
        posts.append({
            "section": "home",
            "label": "Home",
            "slug": "home",
            "title": "Home",
            "content": convert_markdown(readme.read_text(encoding="utf-8"))
        })
    except Exception as e:
        print(f"Warning: Failed to process {readme}: {e}")

for folder, label in SECTIONS.items():
    d = ZETTEL / folder
    if not d.exists():
        continue

    for f in sorted(d.glob("*.md")):
        try:
            posts.append({
                "section": folder,
                "label": label,
                "slug": f.stem,
                "title": f.stem.replace("_", " "),
                "content": convert_markdown(f.read_text(encoding="utf-8"))
            })
        except Exception as e:
            print(f"Warning: Failed to process {f}: {e}")

# Write the generated app.js file with both data and JavaScript logic
js_content = f"""const POSTS = {json.dumps(posts, indent=2)};

const sectionsEl = document.getElementById("sections");
const notesEl = document.getElementById("notes");
const postEl = document.getElementById("post");

const sections = [...new Set(POSTS.map(p => p.section))];

function renderSections() {{
  sectionsEl.innerHTML = sections.map(s => {{
    const post = POSTS.find(p => p.section === s);
    const label = post ? post.label : s;
    return `<button onclick="showSection('${{s}}')">${{label}}</button>`;
  }}).join("");
}}

function showSection(section) {{
  const filtered = POSTS.filter(p => p.section === section && p.slug !== "home");
  notesEl.innerHTML = filtered
    .map(p => `<a href="#/${{p.section}}/${{p.slug}}">${{p.title}}</a>`)
    .join("");
  
  // If home section, show the home post content
  if (section === "home") {{
    const homePost = POSTS.find(p => p.section === "home" && p.slug === "home");
    if (homePost) {{
      postEl.innerHTML = `<h2>${{homePost.title}}</h2>${{homePost.content}}`;
    }} else {{
      postEl.innerHTML = "";
    }}
  }} else {{
    postEl.innerHTML = "";
  }}
}}

function showPost(section, slug) {{
  const p = POSTS.find(p => p.section === section && p.slug === slug);
  if (!p) return;
  postEl.innerHTML = `<h2>${{p.title}}</h2>${{p.content}}`;
}}

function celebrate() {{
  const symbols = ["🚀","✨","🔥","💡","🛠️"];
  for (let i = 0; i < 25; i++) {{
    const p = document.createElement("div");
    p.className = "particle";
    p.textContent = symbols[Math.floor(Math.random() * symbols.length)];
    p.style.left = (window.innerWidth * Math.random()) + "px";
    p.style.top = (window.innerHeight - 20) + "px";
    p.style.animationDuration = (0.9 + Math.random()*0.7) + "s";
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 1500);
  }}
}}

window.addEventListener("hashchange", () => {{
  const [, s, slug] = location.hash.split("/");
  if (slug) showPost(s, slug);
  else if (s) showSection(s);
}});

// Initialize on load
if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", () => {{
    renderSections();
    const hash = location.hash;
    if (hash) {{
      const [, s, slug] = hash.split("/");
      if (slug) showPost(s, slug);
      else if (s) showSection(s);
    }} else {{
      showSection("home");
    }}
  }});
}} else {{
  renderSections();
  const hash = location.hash;
  if (hash) {{
    const [, s, slug] = hash.split("/");
    if (slug) showPost(s, slug);
    else if (s) showSection(s);
  }} else {{
    showSection("home");
  }}
}}
"""

output_file = SITE / "app.js"
output_file.write_text(js_content, encoding="utf-8")
print(f"Generated {len(posts)} posts to {output_file}")

