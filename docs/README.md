# CubeForge Docs

The source for CubeForge's GitHub Pages site. Built with Jekyll, using
GitHub Pages' own supported theme (`minima`) and gem set, so it needs no
custom CI/build step - GitHub builds and deploys it automatically on
every push to the configured branch.

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

The formal specification itself (`specs/`) is **not** duplicated here -
this site links out to it. `specs/` is the source of truth for behavior;
these pages are the approachable tour.
