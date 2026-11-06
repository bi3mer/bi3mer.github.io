// Searches /index.json in the browser. Every word in the query has to match.
const box = document.getElementById("search-box");
const results = document.getElementById("search-results");
let pages = [];

function draw() {
  const words = box.value.toLowerCase().split(/\s+/).filter(Boolean);
  results.replaceChildren();
  if (words.length === 0) return;

  const scored = [];
  for (const page of pages) {
    const title = page.title.toLowerCase();
    const body = page.content.toLowerCase();
    if (!words.every(w => title.includes(w) || body.includes(w))) continue;
    scored.push([words.filter(w => title.includes(w)).length, page]);
  }
  scored.sort((a, b) => b[0] - a[0]);

  for (const [, page] of scored.slice(0, 50)) {
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = page.url;
    link.textContent = page.title;
    const meta = document.createElement("span");
    meta.className = "card-meta";
    meta.textContent = page.date;
    item.append(link, meta);
    results.append(item);
  }
}

fetch("/index.json")
  .then(response => response.json())
  .then(data => { pages = data; draw(); });
box.addEventListener("input", draw);
