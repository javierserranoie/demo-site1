from pathlib import Path
import markdown
import json
import os
import shutil

ZETTEL = Path(os.getenv("PERSONAL_SITE_ZETTEL", "/zettel"))
SITE = Path("/app/site")
SITE.mkdir(parents=True, exist_ok=True)

# Copy logo if it exists in the app directory
logo_source = Path("/app/logo004.png")
logo_dest = SITE / "logo004.png"
if logo_source.exists():
    shutil.copy(logo_source, logo_dest)
    print(f"Copied logo to {logo_dest}")

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
  hideLanding();
  const filtered = POSTS.filter(p => p.section === section);
  notesEl.innerHTML = filtered
    .map(p => `<a href="#/${{p.section}}/${{p.slug}}">${{p.title}}</a>`)
    .join("");
  
  // Hide article box and show notes index when section is selected
  postEl.innerHTML = "";
  postEl.style.display = "none";
  notesEl.style.display = "block";
  // Hide back to top button when showing section
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) backToTopBtn.classList.remove("visible");
  
  // Update hash to reflect section change
  const newHash = `#/${{section}}`;
  if (location.hash !== newHash) {{
    location.hash = newHash;
  }}
}}

function showPost(section, slug) {{
  hideLanding();
  const p = POSTS.find(p => p.section === section && p.slug === slug);
  if (!p) {{
    postEl.style.display = "none";
    notesEl.style.display = "block";
    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) backToTopBtn.classList.remove("visible");
    return;
  }}
  
  // Check if this is the same article already displayed
  const currentHash = location.hash;
  const newHash = `#/${{section}}/${{slug}}`;
  
  // Show article and hide notes index when article is selected
  postEl.style.display = "block";
  postEl.innerHTML = `<h2>${{p.title}}</h2>${{p.content}}`;
  notesEl.style.display = "none";
  
  // Update hash even if it's the same article (to trigger re-display)
  if (currentHash !== newHash) {{
    location.hash = newHash;
  }}
  
  // Reset scroll position when showing article (button will hide at top)
  window.scrollTo({{ top: 0, behavior: "smooth" }});
  // Button visibility will be handled by scroll listener
}}


function showLanding() {{
  const landingEl = document.getElementById("landing");
  const notesEl = document.getElementById("notes");
  const postEl = document.getElementById("post");
  const navEl = document.getElementById("sections");
  
  if (landingEl) {{
    landingEl.style.display = "block";
    notesEl.style.display = "none";
    postEl.style.display = "none";
    // Keep navigation buttons visible below landing page
    if (navEl) navEl.style.display = "flex";
    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) backToTopBtn.classList.remove("visible");
    window.scrollTo({{ top: 0, behavior: "smooth" }});
  }}
}}

function hideLanding() {{
  const landingEl = document.getElementById("landing");
  if (landingEl) {{
    landingEl.style.display = "none";
  }}
}}

window.addEventListener("hashchange", () => {{
  const hash = location.hash;
  if (!hash || hash === "#/" || hash === "#") {{
    showLanding();
  }} else {{
    const [, s, slug] = hash.split("/");
    hideLanding();
    if (slug) {{
      showPost(s, slug);
    }} else if (s) {{
      showSection(s);
    }}
  }}
}});

// Also handle clicks on note links to ensure they work even if hash doesn't change
document.addEventListener("click", (e) => {{
  const link = e.target.closest("#notes a");
  if (link) {{
    const href = link.getAttribute("href");
    if (href && href.startsWith("#/")) {{
      const [, s, slug] = href.split("/");
      if (slug) {{
        // Force show even if it's the same article
        e.preventDefault();
        showPost(s, slug);
      }}
    }}
  }}
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
  if (hash && hash !== "#/" && hash !== "#") {{
    const [, s, slug] = hash.split("/");
    if (slug) showPost(s, slug);
    else if (s) showSection(s);
  }} else {{
    // Show landing page on initial load
    showLanding();
  }}
  
  // Initialize back to top button - show when article is visible and scrolled down
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) {{
    function updateBackToTopButton() {{
      // Show button when article is visible AND scrolled down from top
      if (postEl.style.display === "block" && window.pageYOffset > 50) {{
        backToTopBtn.classList.add("visible");
      }} else {{
        backToTopBtn.classList.remove("visible");
      }}
    }}
    
    window.addEventListener("scroll", updateBackToTopButton);
    // Also check on hash change
    window.addEventListener("hashchange", updateBackToTopButton);
    // Initial check
    updateBackToTopButton();
  }}
  
  // Make title link work
  const homeLink = document.getElementById("homeLink");
  if (homeLink) {{
    homeLink.addEventListener("click", (e) => {{
      e.preventDefault();
      location.hash = "#/";
      showLanding();
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

