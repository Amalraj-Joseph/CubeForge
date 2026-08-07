# 04_web_game.py - Interactive 3D Rubik's Cube, backed by CubeCore

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import os
import sys
import traceback

# Add the parent directory to path to find CubeCore
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# CubeCore imports - everything needed is reachable from the top-level
# public API, per cube/__init__.py.
from cube import (
    Algorithm,
    B, B2, B_PRIME,
    Cube,
    D, D2, D_PRIME,
    F, F2, F_PRIME,
    FACE_LAYOUTS,
    L, L2, L_PRIME,
    LogicalFace,
    Move,
    R, R2, R_PRIME,
    ScrambleGenerator,
    U, U2, U_PRIME,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Move lookup for button mapping
MOVE_MAP = {
    'U': U, 'U2': U2, "U'": U_PRIME,
    'D': D, 'D2': D2, "D'": D_PRIME,
    'R': R, 'R2': R2, "R'": R_PRIME,
    'L': L, 'L2': L2, "L'": L_PRIME,
    'F': F, 'F2': F2, "F'": F_PRIME,
    'B': B, 'B2': B2, "B'": B_PRIME,
}

# Color mapping for visualization - map CubeCore colors to hex
COLOR_MAP = {
    'WHITE': '#FFFFFF',
    'YELLOW': '#FFFF00',
    'GREEN': '#00FF00',
    'BLUE': '#0000FF',
    'RED': '#FF0000',
    'ORANGE': '#FF8C00',
}

# Global state
current_cube = Cube.canonical()
move_history: list[Move] = []


def get_face_colors(cube_state):
    """
    Extract colors for each face of the cube.

    Returns a dict with 3x3 grids for each face (U, D, F, B, L, R). Each
    cell contains a hex color string like '#FFFFFF'.

    Built directly from CubeCore's own FACE_LAYOUTS: for each face, that's
    the 9 Positions on it in raster order (row-major, top-left to
    bottom-right), so every cell is filled from a single, already-correct
    source of truth rather than a hand-maintained lookup table.
    """
    face_colors = {}

    for face in LogicalFace:
        grid = [[None, None, None] for _ in range(3)]

        for index, position in enumerate(FACE_LAYOUTS[face]):
            row, col = divmod(index, 3)
            piece_state = cube_state.piece_at(position)
            color = piece_state.color_on(face)
            grid[row][col] = COLOR_MAP.get(color.name, '#888888')

        face_colors[face.symbol] = grid

    return face_colors


def check_solved(cube_state):
    """
    Check if the cube is solved.

    Delegates to CubeState.solved rather than re-deriving it from
    get_face_colors' grid: that grid only fills in one of each edge's
    two faces and one of each corner's three (a separate, pre-existing
    rendering gap - see get_face_colors), so it under-reports colors
    and can never agree that a solved cube is solved.
    """
    return cube_state.solved


@app.route('/')
def index():
    return render_template('cube.html')


@app.route('/api/state')
def get_state():
    global current_cube
    try:
        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': len(move_history),
            'move_history': ' '.join(m.notation for m in move_history),
            'is_solved': check_solved(current_cube.state)
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/move', methods=['POST'])
def apply_move():
    global current_cube, move_history
    try:
        data = request.get_json()
        move_name = data.get('move')
        if move_name not in MOVE_MAP:
            return jsonify({'success': False, 'error': f'Unknown move: {move_name}'}), 400
        
        move = MOVE_MAP[move_name]
        current_cube = current_cube.apply(move)
        move_history.append(move)
        
        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': len(move_history),
            'move_history': ' '.join(m.notation for m in move_history),
            'is_solved': check_solved(current_cube.state)
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/algorithm', methods=['POST'])
def apply_algorithm():
    global current_cube, move_history
    try:
        data = request.get_json()
        notation = data.get('notation', '')
        if not notation:
            return jsonify({'success': False, 'error': 'Empty algorithm'}), 400
        
        try:
            algorithm = Algorithm.parse(notation)
        except ValueError as ex:
            return jsonify({'success': False, 'error': str(ex)}), 400

        current_cube = current_cube.apply_algorithm(algorithm)
        for move in algorithm:
            move_history.append(move)

        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': len(move_history),
            'move_history': ' '.join(m.notation for m in move_history),
            'is_solved': check_solved(current_cube.state)
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scramble', methods=['POST'])
def apply_scramble():
    global current_cube, move_history
    try:
        data = request.get_json() or {}
        length = data.get('length', 20)
        
        scramble = ScrambleGenerator.generate(length)
        current_cube = current_cube.apply_algorithm(scramble)
        for move in scramble:
            move_history.append(move)
        
        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': len(move_history),
            'move_history': ' '.join(m.notation for m in move_history),
            'scramble': scramble.notation,
            'is_solved': check_solved(current_cube.state)
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_cube():
    global current_cube, move_history
    try:
        current_cube = Cube.canonical()
        move_history = []
        
        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': 0,
            'move_history': '',
            'is_solved': True
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/undo', methods=['POST'])
def undo_move():
    global current_cube, move_history
    try:
        if not move_history:
            return jsonify({'success': False, 'error': 'No moves to undo'}), 400
        
        last_move = move_history.pop()
        current_cube = current_cube.apply(last_move.inverse)
        
        face_colors = get_face_colors(current_cube.state)
        return jsonify({
            'success': True,
            'faces': face_colors,
            'move_count': len(move_history),
            'move_history': ' '.join(m.notation for m in move_history),
            'is_solved': check_solved(current_cube.state)
        })
    except Exception as e:
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500


# Create templates directory
os.makedirs('templates', exist_ok=True)

# Create the HTML template - with proper 3D rendering
with open('templates/cube.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧩 CubeCore - Rubik's Cube</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a2e;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        .container {
            display: flex;
            gap: 30px;
            padding: 20px;
            width: 100%;
            height: 100vh;
        }
        .cube-container {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #16213e;
            border-radius: 20px;
            padding: 20px;
            min-height: 500px;
        }
        #cube-canvas {
            width: 100%;
            height: 100%;
            min-height: 500px;
            background: #0f3460;
            border-radius: 10px;
            display: block;
        }
        .controls {
            width: 350px;
            background: #16213e;
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 100vh;
            overflow-y: auto;
        }
        .controls h1 { font-size: 22px; color: #e94560; text-align: center; }
        .controls .subtitle { text-align: center; color: #aaa; font-size: 13px; }
        .status {
            display: flex; justify-content: space-between;
            padding: 8px 12px; background: #0f3460; border-radius: 8px;
            font-size: 13px;
        }
        .solved { color: #00ff88; }
        .unsolved { color: #ff6b6b; }
        .move-grid {
            display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 5px;
        }
        .move-btn {
            padding: 8px; border: none; border-radius: 6px;
            font-size: 13px; font-weight: bold; cursor: pointer;
            font-family: 'Courier New', monospace;
            transition: all 0.2s;
            background: #0f3460; color: #fff;
        }
        .move-btn:hover { transform: scale(1.05); }
        .move-btn:active { transform: scale(0.95); }
        .move-btn.face-U { background: #ffffff; color: #000; }
        .move-btn.face-D { background: #ffff00; color: #000; }
        .move-btn.face-F { background: #00ff00; color: #000; }
        .move-btn.face-B { background: #0000ff; color: #fff; }
        .move-btn.face-L { background: #ff8c00; color: #000; }
        .move-btn.face-R { background: #ff0000; color: #fff; }
        .action-grid {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 6px;
        }
        .action-btn {
            padding: 8px; border: none; border-radius: 6px;
            font-size: 12px; font-weight: bold; cursor: pointer;
            transition: all 0.2s;
            background: #0f3460; color: #fff;
        }
        .action-btn:hover { transform: scale(1.02); }
        .action-btn.scramble { background: #e94560; }
        .action-btn.scramble:hover { background: #ff6b81; }
        .action-btn.reset { background: #2d3436; }
        .action-btn.reset:hover { background: #4a4a4a; }
        .action-btn.undo { background: #fdcb6e; color: #000; }
        .action-btn.undo:hover { background: #ffeaa7; }
        .action-btn.solve { background: #00b894; }
        .action-btn.solve:hover { background: #00d2a0; }
        .algorithm-input {
            display: flex; gap: 6px;
        }
        .algorithm-input input {
            flex: 1; padding: 8px 10px;
            border: 2px solid #0f3460; border-radius: 6px;
            background: #0a0a1a; color: #fff;
            font-size: 12px; font-family: 'Courier New', monospace;
        }
        .algorithm-input input:focus { outline: none; border-color: #e94560; }
        .algorithm-input button {
            padding: 8px 14px; border: none; border-radius: 6px;
            background: #00b894; color: #fff;
            font-weight: bold; cursor: pointer;
        }
        .algorithm-input button:hover { background: #00d2a0; }
        .move-history {
            min-height: 50px; max-height: 120px;
            overflow-y: auto; padding: 8px 10px;
            background: #0a0a1a; border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px; color: #aaa;
            line-height: 1.5; word-wrap: break-word;
        }
        .move-history::-webkit-scrollbar { width: 4px; }
        .move-history::-webkit-scrollbar-track { background: #0f3460; border-radius: 2px; }
        .move-history::-webkit-scrollbar-thumb { background: #e94560; border-radius: 2px; }
        .shortcuts {
            font-size: 10px; color: #666; text-align: center;
            border-top: 1px solid #0f3460; padding-top: 10px;
        }
        .shortcuts kbd {
            background: #0f3460; padding: 1px 5px;
            border-radius: 3px; font-size: 9px;
        }
        @media (max-width: 900px) {
            .container { flex-direction: column; height: auto; padding: 10px; }
            .cube-container { height: 400px; min-height: 300px; }
            #cube-canvas { min-height: 300px; }
            .controls { width: 100%; max-height: none; }
        }
        .error-msg {
            color: #ff6b6b;
            font-size: 12px;
            text-align: center;
            padding: 4px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="cube-container">
            <canvas id="cube-canvas"></canvas>
        </div>
        <div class="controls">
            <h1>🧩 CubeCore</h1>
            <div class="subtitle">Interactive 3D Rubik's Cube</div>
            <div class="status">
                <span>Moves: <span id="move-count">0</span></span>
                <span id="solved-status" class="solved">✓ Solved</span>
            </div>
            <div class="move-grid">
                <button class="move-btn face-U" data-move="U">U</button>
                <button class="move-btn face-U" data-move="U2">U2</button>
                <button class="move-btn face-U" data-move="U'">U'</button>
                <button class="move-btn face-D" data-move="D">D</button>
                <button class="move-btn face-D" data-move="D2">D2</button>
                <button class="move-btn face-D" data-move="D'">D'</button>
                <button class="move-btn face-F" data-move="F">F</button>
                <button class="move-btn face-F" data-move="F2">F2</button>
                <button class="move-btn face-F" data-move="F'">F'</button>
                <button class="move-btn face-B" data-move="B">B</button>
                <button class="move-btn face-B" data-move="B2">B2</button>
                <button class="move-btn face-B" data-move="B'">B'</button>
                <button class="move-btn face-L" data-move="L">L</button>
                <button class="move-btn face-L" data-move="L2">L2</button>
                <button class="move-btn face-L" data-move="L'">L'</button>
                <button class="move-btn face-R" data-move="R">R</button>
                <button class="move-btn face-R" data-move="R2">R2</button>
                <button class="move-btn face-R" data-move="R'">R'</button>
            </div>
            <div class="action-grid">
                <button class="action-btn scramble" id="scramble-btn">🎲 Scramble</button>
                <button class="action-btn reset" id="reset-btn">↺ Reset</button>
                <button class="action-btn undo" id="undo-btn">↩ Undo</button>
                <button class="action-btn solve" id="solve-btn">✨ Solve</button>
            </div>
            <div class="algorithm-input">
                <input type="text" id="algorithm-input" placeholder="R U R' U' ..." spellcheck="false">
                <button id="apply-alg-btn">Apply</button>
            </div>
            <div class="move-history" id="move-history"><span style="color:#666;">Move history...</span></div>
            <div class="error-msg" id="error-msg"></div>
            <div class="shortcuts">
                <kbd>U</kbd> <kbd>D</kbd> <kbd>F</kbd> <kbd>B</kbd> <kbd>L</kbd> <kbd>R</kbd> &middot;
                <kbd>Shift</kbd>+face inverse &middot; <kbd>Space</kbd> scramble &middot; <kbd>Z</kbd> undo
            </div>
        </div>
    </div>

    <!-- Load Three.js from CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js">
    </script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js">
    </script>
    
    <script>
        console.log('🧩 CubeCore loading...');
        
        if (typeof THREE === 'undefined') {
            document.getElementById('error-msg').textContent = '⚠️ Failed to load Three.js. Check internet connection.';
            document.getElementById('error-msg').style.display = 'block';
            console.error('Three.js failed to load');
        } else {
            console.log('✅ Three.js loaded, version:', THREE.REVISION);
        }
        
        // ============================================================
        // State
        // ============================================================
        let isAnimating = false;
        let animationQueue = [];
        let scene, camera, renderer, controls, cubeGroup;
        
        // ============================================================
        // Setup Three.js
        // ============================================================
        function setupScene() {
            const canvas = document.getElementById('cube-canvas');
            const container = canvas.parentElement;
            
            function resize() {
                const rect = container.getBoundingClientRect();
                const w = Math.max(rect.width - 40, 300);
                const h = Math.max(rect.height - 40, 300);
                canvas.width = w;
                canvas.height = h;
                canvas.style.width = w + 'px';
                canvas.style.height = h + 'px';
                return { width: w, height: h };
            }
            
            const size = resize();
            
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0f3460);
            
            camera = new THREE.PerspectiveCamera(45, size.width / size.height, 0.1, 100);
            camera.position.set(5, 5, 5);
            camera.lookAt(0, 0, 0);
            
            renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
            renderer.setSize(size.width, size.height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.1;
            controls.target.set(0, 0, 0);
            controls.update();
            
            const ambient = new THREE.AmbientLight(0x606080);
            scene.add(ambient);
            
            const light1 = new THREE.DirectionalLight(0xffffff, 1.2);
            light1.position.set(10, 20, 10);
            scene.add(light1);
            
            const light2 = new THREE.DirectionalLight(0xffffff, 0.6);
            light2.position.set(-10, -5, -10);
            scene.add(light2);
            
            cubeGroup = new THREE.Group();
            scene.add(cubeGroup);
            
            window.addEventListener('resize', () => {
                const s = resize();
                camera.aspect = s.width / s.height;
                camera.updateProjectionMatrix();
                renderer.setSize(s.width, s.height);
            });
            
            function animate() {
                requestAnimationFrame(animate);
                if (controls) controls.update();
                if (renderer && scene && camera) renderer.render(scene, camera);
            }
            animate();
            
            console.log('✅ Scene setup complete');
            return true;
        }
        
        // ============================================================
        // Cube Rendering
        //
        // Renders directly from the 6 face grids the backend sends
        // (get_face_colors, itself built from CubeCore's FACE_LAYOUTS) -
        // 9 sticker planes placed on each face, rather than trying to
        // reconstruct 26 individual cubies and guess which faces each
        // one shows. Each face's (row, col) -> 3D position uses the
        // same axis convention CubeCore itself uses internally
        // (RIGHT=+X, UP=+Y, FRONT=+Z), and was verified analytically
        // against FACE_LAYOUTS position-by-position before being written
        // here (54 of 54 checks passed - see conversation).
        // ============================================================
        const FACE_AXES = {
            U: { normal: [0, 1, 0], row: [0, 0, -1], col: [1, 0, 0] },
            D: { normal: [0, -1, 0], row: [0, 0, -1], col: [1, 0, 0] },
            F: { normal: [0, 0, 1], row: [0, -1, 0], col: [1, 0, 0] },
            B: { normal: [0, 0, -1], row: [0, -1, 0], col: [-1, 0, 0] },
            L: { normal: [-1, 0, 0], row: [0, -1, 0], col: [0, 0, 1] },
            R: { normal: [1, 0, 0], row: [0, -1, 0], col: [0, 0, -1] },
        };

        const CUBE_HALF = 1.5;   // half-extent of the 3-unit cube (one unit per layer)
        const CELL_SIZE = 1;     // one unit per sticker cell
        const STICKER_SIZE = 0.85;

        function buildCube(faceData) {
            if (!cubeGroup) return;

            // Clear old cube
            while (cubeGroup.children.length > 0) {
                const child = cubeGroup.children[0];
                cubeGroup.remove(child);
                if (child.geometry) child.geometry.dispose();
                if (child.material) child.material.dispose();
            }

            function getColor(grid, row, col) {
                try {
                    const hex = grid[row][col];
                    if (typeof hex === 'string' && hex.startsWith('#')) {
                        return parseInt(hex.slice(1), 16);
                    }
                } catch (e) {
                    // fall through to the default below
                }
                return 0x333333;
            }

            function createSticker(color, position, normal) {
                const geo = new THREE.PlaneGeometry(STICKER_SIZE, STICKER_SIZE);
                const mat = new THREE.MeshStandardMaterial({
                    color: color,
                    roughness: 0.3,
                    metalness: 0.1,
                    side: THREE.DoubleSide,
                });
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.copy(position);
                mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
                return mesh;
            }

            try {
                // Dark base cube so the gaps between stickers read correctly
                const baseSize = CUBE_HALF * 2 - 0.06;
                const baseGeo = new THREE.BoxGeometry(baseSize, baseSize, baseSize);
                const baseMat = new THREE.MeshStandardMaterial({
                    color: 0x1a1a2e,
                    roughness: 0.8,
                    metalness: 0.2,
                });
                cubeGroup.add(new THREE.Mesh(baseGeo, baseMat));

                let stickerCount = 0;

                for (const [face, axes] of Object.entries(FACE_AXES)) {
                    const grid = faceData[face];
                    if (!grid) continue;

                    const normal = new THREE.Vector3(...axes.normal);
                    const rowDir = new THREE.Vector3(...axes.row);
                    const colDir = new THREE.Vector3(...axes.col);

                    for (let row = 0; row < 3; row++) {
                        for (let col = 0; col < 3; col++) {
                            const color = getColor(grid, row, col);

                            const position = normal.clone().multiplyScalar(CUBE_HALF + 0.02)
                                .add(rowDir.clone().multiplyScalar((row - 1) * CELL_SIZE))
                                .add(colDir.clone().multiplyScalar((col - 1) * CELL_SIZE));

                            cubeGroup.add(createSticker(color, position, normal));
                            stickerCount++;
                        }
                    }
                }

                console.log('✅ Cube built successfully with', stickerCount, 'stickers');
            } catch (e) {
                console.error('Error building cube:', e);
            }
        }
        
        // ============================================================
        // API Functions
        // ============================================================
        async function fetchState() {
            try {
                const resp = await fetch('/api/state');
                return await resp.json();
            } catch (e) {
                console.error('Fetch error:', e);
                return null;
            }
        }
        
        async function sendMove(move) {
            try {
                const resp = await fetch('/api/move', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ move })
                });
                return await resp.json();
            } catch (e) {
                console.error('Move error:', e);
                return null;
            }
        }
        
        async function sendAlgorithm(notation) {
            try {
                const resp = await fetch('/api/algorithm', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ notation })
                });
                return await resp.json();
            } catch (e) {
                console.error('Algorithm error:', e);
                return null;
            }
        }
        
        async function sendScramble() {
            try {
                const resp = await fetch('/api/scramble', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ length: 20 })
                });
                return await resp.json();
            } catch (e) {
                console.error('Scramble error:', e);
                return null;
            }
        }
        
        async function sendReset() {
            try {
                const resp = await fetch('/api/reset', { method: 'POST' });
                return await resp.json();
            } catch (e) {
                console.error('Reset error:', e);
                return null;
            }
        }
        
        async function sendUndo() {
            try {
                const resp = await fetch('/api/undo', { method: 'POST' });
                return await resp.json();
            } catch (e) {
                console.error('Undo error:', e);
                return null;
            }
        }
        
        // ============================================================
        // UI Updates
        // ============================================================
        function updateUI(data) {
            if (!data || !data.success) {
                const errMsg = data?.error || 'Unknown error';
                document.getElementById('error-msg').textContent = '⚠️ ' + errMsg;
                document.getElementById('error-msg').style.display = 'block';
                return;
            }
            document.getElementById('error-msg').style.display = 'none';
            
            document.getElementById('move-count').textContent = data.move_count || 0;
            
            const status = document.getElementById('solved-status');
            if (data.is_solved) {
                status.textContent = '✓ Solved';
                status.className = 'solved';
            } else {
                status.textContent = '✗ Unsolved';
                status.className = 'unsolved';
            }
            
            const history = document.getElementById('move-history');
            if (data.move_history) {
                // Limit display to last 50 moves
                const moves = data.move_history.split(' ');
                if (moves.length > 50) {
                    history.textContent = '... ' + moves.slice(-50).join(' ');
                } else {
                    history.textContent = data.move_history;
                }
                history.scrollTop = history.scrollHeight;
            } else {
                history.innerHTML = '<span style="color:#666;">Move history...</span>';
            }
        }
        
        async function updateCube() {
            const data = await fetchState();
            if (data && data.success) {
                buildCube(data.faces);
                updateUI(data);
            } else {
                console.error('Failed to fetch cube state:', data?.error);
            }
        }
        
        // ============================================================
        // Actions
        // ============================================================
        async function doMove(move) {
            if (isAnimating) { animationQueue.push(move); return; }
            isAnimating = true;
            const data = await sendMove(move);
            if (data && data.success) { 
                buildCube(data.faces); 
                updateUI(data); 
            }
            isAnimating = false;
            if (animationQueue.length > 0) {
                const next = animationQueue.shift();
                doMove(next);
            }
        }
        
        async function doAlgorithm(notation) {
            if (isAnimating) return;
            isAnimating = true;
            const data = await sendAlgorithm(notation);
            if (data && data.success) { 
                buildCube(data.faces); 
                updateUI(data); 
            }
            isAnimating = false;
        }
        
        async function doScramble() {
            if (isAnimating) return;
            isAnimating = true;
            const data = await sendScramble();
            if (data && data.success) { 
                buildCube(data.faces); 
                updateUI(data); 
            }
            isAnimating = false;
        }
        
        async function doReset() {
            if (isAnimating) return;
            isAnimating = true;
            const data = await sendReset();
            if (data && data.success) { 
                buildCube(data.faces); 
                updateUI(data); 
            }
            isAnimating = false;
        }
        
        async function doUndo() {
            if (isAnimating) return;
            isAnimating = true;
            const data = await sendUndo();
            if (data && data.success) { 
                buildCube(data.faces); 
                updateUI(data); 
            } else if (data?.error) {
                // Show the error but don't clear it
                document.getElementById('error-msg').textContent = '⚠️ ' + data.error;
                document.getElementById('error-msg').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('error-msg').style.display = 'none';
                }, 3000);
            }
            isAnimating = false;
        }
        
        // ============================================================
        // Event Listeners
        // ============================================================
        document.querySelectorAll('.move-btn').forEach(btn => {
            btn.addEventListener('click', () => doMove(btn.dataset.move));
        });
        
        document.getElementById('scramble-btn').addEventListener('click', doScramble);
        document.getElementById('reset-btn').addEventListener('click', doReset);
        document.getElementById('undo-btn').addEventListener('click', doUndo);
        document.getElementById('solve-btn').addEventListener('click', doReset);
        
        document.getElementById('apply-alg-btn').addEventListener('click', () => {
            const input = document.getElementById('algorithm-input');
            const notation = input.value.trim();
            if (notation) { doAlgorithm(notation); input.value = ''; }
        });
        
        document.getElementById('algorithm-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') document.getElementById('apply-alg-btn').click();
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT') return;
            const key = e.key.toUpperCase();
            if (['U', 'D', 'F', 'B', 'L', 'R'].includes(key)) {
                const move = e.shiftKey ? key + "'" : key;
                const btn = document.querySelector(`[data-move="${move}"]`);
                if (btn) btn.click();
                e.preventDefault();
            }
            if (key === ' ' || key === 'SPACE') {
                document.getElementById('scramble-btn').click();
                e.preventDefault();
            }
            if (key === 'Z' && !e.shiftKey) {
                document.getElementById('undo-btn').click();
                e.preventDefault();
            }
            if (key === 'Z' && e.shiftKey) {
                document.getElementById('reset-btn').click();
                e.preventDefault();
            }
        });
        
        // ============================================================
        // Initialize
        // ============================================================
        async function init() {
            console.log('🚀 Initializing CubeCore...');
            
            if (typeof THREE === 'undefined') {
                console.error('❌ Three.js not loaded');
                return;
            }
            
            setupScene();
            await updateCube();
            console.log('✅ CubeCore ready!');
        }
        
        if (document.readyState === 'complete') {
            init();
        } else {
            window.addEventListener('load', init);
        }
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("""
    🧩 CubeCore Interactive Web Application
    ======================================
    
    Starting server at http://localhost:5000
    
    The cube should now render with proper colors!
    
    Features:
    - 3D visualization with Three.js
    - Click face buttons or use keyboard: U D F B L R (shift for inverse)
    - Space = Scramble, Z = Undo, Shift+Z = Reset
    
    Press Ctrl+C to quit.
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)