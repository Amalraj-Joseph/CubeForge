# CubeForge Docs

The source for CubeForge's GitHub Pages site. Built with Jekyll, using
GitHub Pages' own supported gem set (`github-pages`) but a fully custom
theme (`_layouts/`, `_includes/`, `assets/css/main.css` - no `minima`),
so it still needs no custom CI/build step - GitHub builds and deploys
it automatically on every push to the configured branch.

The signature visual element is `_includes/cube-diagram.html` (a 3D,
pure-CSS cube rendered from real face-color data, no images) and its
flat-icon sibling `_includes/cube-glyph.html`. Both take plain
comma-separated color-letter grids (`w,y,g,b,r,o`) as Liquid
parameters - see the comment at the top of each file for usage.

## Publishing

In the repository's Settings -> Pages, set:

- **Source:** Deploy from a branch
- **Branch:** `main` (or whichever is the default branch), folder `/docs`

That's it - no GitHub Actions workflow required. GitHub rebuilds the site
within a minute or two of every push that touches `docs/`.

## Local preview

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000/CubeForge/ (the `baseurl` in `_config.yml`
matches how GitHub Pages serves a project site - drop it if you ever move
this to a user/org root site instead).

## Structure

| File                  | Content                                              |
|------------------------|-------------------------------------------------------|
| `index.md`             | Landing page                                          |
| `getting-started.md`   | Install and quickstart                                |
| `architecture.md`      | The domain model, in prose                             |
| `api-reference.md`     | The public API surface (`cube/__init__.py`)            |
| `specification.md`     | Index into the formal spec (`../specs/`)                |
| `web-app.md`           | How to run the `web/` companion app                     |
| `_layouts/`             | `default` (shell), `page` (docs pages), `home` (index)  |
| `_includes/`            | `head`/`header`/`footer`, `cube-diagram`, `cube-glyph`   |
| `assets/css/main.css`   | The entire theme - tokens, layout, typography, cube CSS  |

The formal specification itself (`specs/`) is **not** duplicated here -
this site links out to it. `specs/` is the source of truth for behavior;
these pages are the approachable tour.
