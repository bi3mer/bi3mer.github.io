# Plan: Replace Hugo with a Common Lisp Site Builder, and Bring the Lectures In

Status: step 1 not started. Work happens on the `better-everything` branch.

## Context

This site builds with Hugo 0.137.1 and the PaperMod theme (a git submodule). The lectures live in
a separate repo (`bi3mer/lectures`, published at bi3mer.github.io/lectures) with their own build
(Marp, pandoc, rsync, zip). Some essays already sit in the lectures repo (`cs230/why-with.md`,
`cs230/exit.md`, `cs213/js/why-no-seed.md`). The goal is one site:

- drop Hugo and PaperMod;
- a build program in Common Lisp turns `.md` into finished `.html` and copies every other file
  as is;
- the lectures palette, no CSS framework, CSS grid, mobile first;
- custom subsites (lectures first) that reuse the same build.

Colan is writing the build to learn Common Lisp.

## Who Does What

- **Colan** writes the build program, the template, and the CSS.
- **Claude** gives the broad steps (this file), checks each step when Colan says it is ready,
  and does the file migration at the end.
- **Checking a step** means: read the code for bugs and missed cases, run the build, and compare
  the output against the reference build. Claude points out each problem and why it is one, and
  names the Common Lisp feature that fixes it, but does not rewrite Colan's code unless asked.

## Branch

All work happens on `better-everything`. The Hugo workflow deploys only on pushes to `master`, so
pushing the branch publishes nothing. The live site and the lectures site keep running as they
are until the cutover.

## Decisions

- **Render at build time.** Every `.md` becomes a complete `.html` in `_site/`, so search engines
  and link previews see full pages and readers need no JavaScript.
- **Copy everything else.** Hand-written `.html`, images, PDFs, JS, and the WASM crossword go to
  `_site/` unchanged. A hand-written `.html` is the way to make something custom. A `foo.md` next
  to a `foo.html` is a build error.
- **Common Lisp on SBCL 2.6.9.** Libraries are Colan's call. Standard CL plus UIOP (which ships
  with SBCL) keeps CI to installing SBCL, and the Markdown parser is the part most worth writing.
- **Keep old URLs.** `/posts/<slug>/`, `/posts/leetcode-N/` (the `url =` overrides), `/games/`,
  `/publications/`, `/index.xml`, and every lectures URL (`08-lists.html#27`) keep working.
- **Theme.** Colors from the lectures repo's `themes/lecture.css` (Sanzo Wada combination 151):
  background `#064f6e`, text `#f5ecc2`, accent `#f99d1b`, secondary `#a8c1cc`, code boxes
  `#032837`, stripes and rules `#175b78` and `#38728b`. The lectures repo's `style.css` is a
  working example of the look, written desktop first; the new CSS starts from phone width and
  adds columns with `min-width` media queries.

## What the Build Has to Handle

- 154 Markdown files: 50 posts, 45 problems, 50 YouTube posts, and the top-level pages (home,
  games, projects, publications, open-source tools, go code). 142 use TOML front matter (`+++`),
  12 use YAML (`---`). 5 are drafts.
- Raw HTML inside Markdown: `<script>` tags for Chart.js on 5 LeetCode pages, tables, figures.
- Code fences: Go (169), Python (66), JavaScript (26), C++ (20), Bash (6), C (4), JSON, assembly.
- Footnotes on 18 pages; math on 19 (MathJax).
- Umami analytics in every page head.
- Hugo shortcodes (`youtube` 57, `gameEntry` 15, `simulationEntry` 4, `pdfReader` 4). The parser
  does not need to understand these: the migration turns them into plain HTML.

## Target Layout

```
build/          the Lisp program
templates/      page template(s)
site.css
index.md  games.md  projects.md  publications.md  ...
posts/  problems/  youtube/  essays/     Markdown
images/  pdf/  crossword/  js/            today's static/, copied as is
lectures/       the lectures subsite
_site/          output, gitignored
```

`posts/foo.md` builds to `_site/posts/foo/index.html`. A `url` in front matter overrides that.
During development, the build reads a source folder given on the command line. Claude can make a
scratch copy of `content/` and `static/` merged into this layout whenever Colan wants fresh test
input, so the real files stay put until the migration.

## Steps

Each step ends with a `_site/` that can be served with `python3 -m http.server -d _site` and
checked.

1. **Skeleton.** An ASDF system and package, runnable from the shell and from the REPL.
2. **Copy.** Walk the source tree, skip what should not ship (`.git/`, `.github/`, `.claude/`,
   `build/`, `templates/`, `example-code/`, `_site/`, `README.md`, `PLAN.md`), wipe `_site/`,
   and copy every non-Markdown file. Pathnames are the hard part.
3. **Front matter.** Split it off and parse the TOML and YAML subsets the site uses. ISO dates
   sort correctly as strings.
4. **Pages.** Write each `.md` to its URL inside the template, with the right `<title>`, body
   still raw.
5. **Markdown blocks.** Paragraphs, headings with IDs, fenced code, lists (nested), block quotes,
   tables, thematic breaks, raw HTML blocks. Write tests as you go.
6. **Markdown inlines.** Code spans, emphasis, links, images, autolinks, escapes, footnotes.
7. **CSS.** The theme above: grid, mobile first, readable code blocks and tables at phone width.
8. **Site features.** Skip drafts; list pages for posts, problems, and YouTube, newest first;
   MathJax and Chart.js only where needed; the Umami tag; the RSS feed at `/index.xml`.
9. **Subsites.** A folder can change its template, CSS, output naming (`foo.html` for lectures),
   and skip list. CLOS generic functions fit this well: a subsite is a subclass that overrides
   only what it changes.
10. **CI.** A workflow that installs SBCL and runs the build, replacing `.github/workflows/hugo.yml`.

Later and optional: code highlighting (Go first), a local `serve` command, and a slide renderer to
replace Marp (behavior spelled out in the lectures repo's `future-plans/plan.md`).

## Migration (Claude, Once the Build Is Done)

- `git mv` `content/*` and `static/*` into the target layout, so history follows the files.
- Turn the 80 shortcodes into plain HTML, and convert front matter if the parser supports only one
  format.
- Copy the lectures in under `lectures/`, and move the essays to `essays/`, with the course pages
  linking there.
- Decide the decks: either CI runs Marp on `marp: true` files as its own step, or the decks wait
  for the slide renderer.
- Remove Hugo: `hugo.yml`, the `themes/PaperMod` submodule, `layouts/`, `assets/`, `archetypes/`,
  `.hugo_build.lock`, `public/`, `make_new_problem_post.sh` (or rewrite it for the new layout).
- At cutover: turn off Pages on `bi3mer/lectures`, since a project site would shadow `/lectures/`.
  Keep that repo (archived) or update the decks' starter-file links to
  `github.com/bi3mer/lectures/tree/main/...`.

## Verification

- **Reference build.** Build `master` with Hugo into a scratch folder as the baseline for
  comparing pages. CI pins Hugo 0.137.1; 0.168.0 also builds the site.
- **Per step.** Run the build, serve `_site/`, and compare pages side by side with the reference.
- **Before cutover.** Every URL in the reference build's `sitemap.xml` and every lectures URL
  exists in `_site/`, and a link check over `_site/` (like the one run on the lectures repo)
  comes back clean.
