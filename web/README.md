# CubeForge Web

An interactive, browser-based 3D Rubik's Cube: a Flask REST API backed by
the `cube` engine in [`../core`](../core), rendered client-side with
[Three.js](https://threejs.org/).

This is a companion project, not part of the engine - it depends on Flask
and Flask-CORS, which `core` itself never does.

## Layout

```
web/
  app.py                 Flask app: REST routes only
  requirements.txt       Flask, Flask-CORS, and an editable install of ../core
  templates/
    index.html            Page markup
  static/
    css/style.css          Styling
    js/api.js               fetch() wrappers around the REST API
    js/renderer.js          Three.js scene setup + cube rendering
    js/app.js                UI state, controls, keyboard shortcuts, init
```

## Running it

```bash
cd web
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:5000.

## API

| Route              | Method | Body                        | Description                          |
|---------------------|--------|------------------------------|---------------------------------------|
| `/`                 | GET    | -                            | Serves the page                       |
| `/api/state`        | GET    | -                            | Current cube state                    |
| `/api/move`         | POST   | `{"move": "R"}`              | Apply a single move                   |
| `/api/algorithm`    | POST   | `{"notation": "R U R' U'"}`  | Apply a Singmaster-notation algorithm |
| `/api/scramble`     | POST   | `{"length": 20}` (optional)  | Apply a random scramble               |
| `/api/reset`        | POST   | -                            | Reset to the canonical solved cube    |
| `/api/undo`         | POST   | -                            | Undo the last move                    |

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
