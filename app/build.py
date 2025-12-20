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

# Home section removed - no longer needed

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
  const filtered = POSTS.filter(p => p.section === section);
  notesEl.innerHTML = filtered
    .map(p => `<a href="#/${{p.section}}/${{p.slug}}">${{p.title}}</a>`)
    .join("");
  
  // Hide article box and show notes index when section is selected
  postEl.innerHTML = "";
  postEl.style.display = "none";
  notesEl.style.display = "block";
}}

function showPost(section, slug) {{
  const p = POSTS.find(p => p.section === section && p.slug === slug);
  if (!p) {{
    postEl.style.display = "none";
    notesEl.style.display = "block";
    return;
  }}
  // Show article and hide notes index when article is selected
  postEl.style.display = "block";
  postEl.innerHTML = `<h2>${{p.title}}</h2>${{p.content}}`;
  notesEl.style.display = "none";
  // Reset scroll position when showing article
  window.scrollTo({{ top: 0, behavior: "smooth" }});
}}


window.addEventListener("hashchange", () => {{
  const [, s, slug] = location.hash.split("/");
  if (slug) showPost(s, slug);
  else if (s) showSection(s);
}});

// Back to top button functionality
function scrollToTop() {{
  window.scrollTo({{
    top: 0,
    behavior: "smooth"
  }});
}}

// Initialize on load
function init() {{
  renderSections();
  const hash = location.hash;
  if (hash) {{
    const [, s, slug] = hash.split("/");
    if (slug) showPost(s, slug);
    else if (s) showSection(s);
  }} else {{
    // Hide article box initially, show notes
    postEl.style.display = "none";
    notesEl.style.display = "block";
    // Show first section if available
    if (sections.length > 0) {{
      showSection(sections[0]);
    }}
  }}
  
  // Initialize back to top button - show when scrolling down
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) {{
    window.addEventListener("scroll", () => {{
      // Only show button when article is visible and scrolled down
      if (postEl.style.display === "block" && window.pageYOffset > 300) {{
        backToTopBtn.classList.add("visible");
      }} else {{
        backToTopBtn.classList.remove("visible");
      }}
    }});
  }}
}}

if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", init);
}} else {{
  init();
}}
"""

output_file = SITE / "app.js"
output_file.write_text(js_content, encoding="utf-8")
print(f"Generated {len(posts)} posts to {output_file}")

