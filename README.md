# Personal Site - Zettelkasten Blog

A personal website that exposes a blog from markdown files following a zettelkasten structure.

## Setup

1. Copy your logo to the app directory:
   ```bash
   cp /home/js/Pictures/logos/logo004.png app/logo004.png
   ```

2. If the logo has a white background that needs to be transparent, you can process it:
   ```bash
   # Using ImageMagick (if available)
   convert app/logo004.png -transparent white app/logo004.png
   
   # Or using Python PIL
   python3 -c "from PIL import Image; img = Image.open('app/logo004.png'); img = img.convert('RGBA'); data = img.getdata(); new_data = [(r, g, b, 0) if r > 240 and g > 240 and b > 240 else (r, g, b, a) for r, g, b, a in data]; img.putdata(new_data); img.save('app/logo004.png')"
   ```

3. Build the Docker image:
   ```bash
   make build
   ```

4. Deploy to Docker Swarm:
   ```bash
   docker stack deploy -c docker-compose.yml personal-site
   ```

## Structure

- `app/` - Application source files
  - `build.py` - Builds the static site from markdown files
  - `index.html` - Main HTML template
  - `style.css` - Styling
  - `logo004.png` - Logo file (needs to be copied here)
- `docker-compose.yml` - Docker Swarm configuration
- `Makefile` - Build and deployment commands

## Zettelkasten Structure

The site expects markdown files in `$HOME/documents` with this structure:
- `README.md` - Home page content
- `00-fly/` - Fleeting notes
- `01-literature/` - Literature notes
- `02-permanent/` - Permanent notes
- `03-structure/` - Structure notes
