// Three.js scene setup and cube rendering.
//
// buildCube() renders directly from the 6 face grids the backend sends
// (get_face_colors in app.py, itself built from CubeCore's own
// FACE_LAYOUTS) - 9 sticker planes placed on each face, rather than
// reconstructing 26 individual cubies and guessing which faces each one
// shows. Each face's (row, col) -> 3D position uses the same axis
// convention CubeCore uses internally (RIGHT=+X, UP=+Y, FRONT=+Z), and
// was verified analytically against every FACE_LAYOUTS entry before
// being written here.

let scene, camera, renderer, controls, cubeGroup;

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

    return true;
}

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

        console.log('Cube built with', stickerCount, 'stickers');
    } catch (e) {
        console.error('Error building cube:', e);
    }
}
