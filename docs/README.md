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
`_includes/webapp-mockup.html` reuses `cube-diagram.html` inside a
static HTML/CSS reproduction of the `web/` app's UI chrome (fixed
sample data, not a screenshot).

## Publishing

In the repository's Settings -> Pages, set:

- **Source:** Deploy from a branch
- **Branch:** `main` (or whichever is the default branch), folder `/docs`
- **Custom domain:** `cubeforge.amalraj.dev` (backed by `docs/CNAME`, which
  GitHub Pages requires to live in the published source folder; DNS points
  the `cubeforge` subdomain at GitHub Pages via a `CNAME` record)

That's it - no GitHub Actions workflow required. GitHub rebuilds the site
within a minute or two of every push that touches `docs/`.

## Local preview

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000/ (`baseurl` in `_config.yml` is empty
since the site is served from the `cubeforge.amalraj.dev` custom domain
at the root, not from a `/CubeForge` project-page path).

## Structure

| File                  | Content                                              |
|------------------------|-------------------------------------------------------|
| `index.md`             | Landing page                                          |
| `getting-started.md`   | Install and quickstart                                |
| `architecture.md`      | The domain model, in prose                             |
| `api-reference.md`     | The public API surface (`cube/__init__.py`)            |
| `specification.md`     | Index into the spec, linking to the rendered docs below |
| `specification/*.md`   | Every `specs/v1/` document, rendered in full on-site    |
| `web-app.md`           | How to run the `web/` companion app, plus a static UI mockup |
| `_layouts/`             | `default` (shell), `page` (docs pages), `home` (index)  |
| `_includes/`            | `head`/`header`/`footer`, `cube-diagram`, `cube-glyph`, `webapp-mockup` |
| `assets/css/main.css`   | The entire theme - tokens, layout, typography, cube CSS  |

`specification/*.md` is a verbatim copy of each `specs/v1/*.md` document
(front matter and prev/next nav added, content untouched) so visitors can
read the actual specification without leaving the site. `specs/` remains
the source of truth - if the two ever drift, `specs/` wins; re-copy the
affected file(s) here to resync.
