---
layout: page
title: Web App
---

# Web App

`web/` is an interactive, browser-based 3D Rubik's Cube: a Flask REST
API backed by `core/`, rendered client-side with
[Three.js](https://threejs.org/). It's a companion project - it depends
on Flask and Flask-CORS, which the engine itself never does, and it
consumes `core/` purely through [the public API]({{ '/api-reference.html' | relative_url }}).

{% include webapp-mockup.html %}

A static HTML/CSS reproduction of the running app - not a screenshot -
built from the same six sticker colors and cube-diagram component used
throughout this site, with fixed sample data standing in for a live
session.

## Running it

```bash
cd web
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open <http://localhost:5000>. `requirements.txt` installs `core/`
in editable mode (`-e ../core`) alongside Flask, so it always reflects
whatever's currently in `core/cube/`.

## Controls

Click a face button, or use the keyboard: `U D F B L R` (hold Shift for
the inverse turn), Space to scramble, `Z` to undo, Shift+`Z` to reset.
The algorithm input box accepts standard Singmaster notation
(`R U R' U'`).

## How it's built

| Layer | File(s) | Job |
|---|---|---|
| Backend | `web/app.py` | REST routes: construct/apply/inspect a `Cube`, nothing else |
| Markup | `web/templates/index.html` | Page structure |
| Style | `web/static/css/style.css` | All CSS |
| API client | `web/static/js/api.js` | `fetch()` wrappers around the REST routes |
| Renderer | `web/static/js/renderer.js` | Three.js scene setup + cube rendering |
| Controls | `web/static/js/app.js` | UI state, event listeners, keyboard shortcuts, init |

The renderer places 9 sticker planes directly on each of the cube's 6
faces from the backend's face-color grids, using the same coordinate
convention (`RIGHT=+X, UP=+Y, FRONT=+Z`) the engine itself uses
internally for whole-cube transformations - rather than reconstructing
26 individual sub-cubes and guessing which faces each one shows, which
is a common source of subtle rendering bugs in cube visualizers.

## API

| Route | Method | Body | Description |
|---|---|---|---|
| `/` | GET | - | Serves the page |
| `/api/state` | GET | - | Current cube state |
| `/api/move` | POST | `{"move": "R"}` | Apply a single move |
| `/api/algorithm` | POST | `{"notation": "R U R' U'"}` | Apply a Singmaster-notation algorithm |
| `/api/scramble` | POST | `{"length": 20}` (optional) | Apply a random scramble |
| `/api/reset` | POST | - | Reset to the canonical solved cube |
| `/api/undo` | POST | - | Undo the last move |

Every response has the shape:

```json
{
  "success": true,
  "faces": {"U": [[...],[...],[...]], "D": [...], "F": [...], "B": [...], "L": [...], "R": [...]},
  "move_count": 0,
  "move_history": "",
  "is_solved": true
}
```

or, on failure, `{"success": false, "error": "..."}` with a 4xx/5xx status.
