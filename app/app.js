const sectionsEl = document.getElementById("sections");
const notesEl = document.getElementById("notes");
const postEl = document.getElementById("post");

const sections = [...new Set(POSTS.map(p => p.section))];

function renderSections() {
  sectionsEl.innerHTML = sections.map(s =>
    `<button onclick="showSection('${s}')">${s}</button>`
  ).join("");
}

function showSection(section) {
  notesEl.innerHTML = POSTS
    .filter(p => p.section === section && p.slug !== "home")
    .map(p => `<a href="#/${section}/${p.slug}">${p.title}</a>`)
    .join("");
  postEl.innerHTML = "";
}

function showPost(section, slug) {
  const p = POSTS.find(p => p.section === section && p.slug === slug);
  if (!p) return;
  postEl.innerHTML = `<h2>${p.title}</h2>${p.content}`;
}

window.addEventListener("hashchange", () => {
  const [, s, slug] = location.hash.split("/");
  if (slug) showPost(s, slug);
  else if (s) showSection(s);
});

renderSections();
showSection("home");

/* your existing celebration() unchanged */

