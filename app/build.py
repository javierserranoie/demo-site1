from pathlib import Path
import markdown
import json
import os

ZETTEL = Path(os.getenv("PERSONAL_SITE_ZETTEL", "/zettel"))
#SITE = Path("app/site")
#SITE.mkdir(exist_ok=True)

SECTIONS = {
    "00-fly": "Fleeting",
    "01-literature": "Literature",
    "02-permanent": "Permanent",
    "03-structure": "Structure",
}

md = markdown.Markdown(extensions=["fenced_code", "tables"])

posts = []

# README → home
readme = ZETTEL / "README.md"
if readme.exists():
    posts.append({
        "section": "home",
        "label": "Home",
        "slug": "home",
        "title": "Home",
        "content": md.convert(readme.read_text())
    })

for folder, label in SECTIONS.items():
    d = ZETTEL / folder
    if not d.exists():
        continue

    for f in sorted(d.glob("*.md")):
        posts.append({
            "section": folder,
            "label": label,
            "slug": f.stem,
            "title": f.stem.replace("_", " "),
            "content": md.convert(f.read_text())
        })

(Path("/app/site/app.js")).write_text(
    "const POSTS = " + json.dumps(posts, indent=2),
    encoding="utf-8"
)

