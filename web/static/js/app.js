// UI updates, user actions, and app initialization. Depends on api.js
// (fetchState/sendMove/...) and renderer.js (setupScene/buildCube).

let isAnimating = false;
let animationQueue = [];

function updateUI(data) {
    if (!data || !data.success) {
        const errMsg = data?.error || 'Unknown error';
        document.getElementById('error-msg').textContent = errMsg;
        document.getElementById('error-msg').style.display = 'block';
        return;
    }
    document.getElementById('error-msg').style.display = 'none';

    document.getElementById('move-count').textContent = data.move_count || 0;

    const status = document.getElementById('solved-status');
    if (data.is_solved) {
        status.textContent = 'Solved';
        status.className = 'solved';
    } else {
        status.textContent = 'Unsolved';
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
        const errMsg = document.getElementById('error-msg');
        errMsg.textContent = data.error;
        errMsg.style.display = 'block';
        setTimeout(() => { errMsg.style.display = 'none'; }, 3000);
    }
    isAnimating = false;
}

function attachEventListeners() {
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
}

async function init() {
    if (typeof THREE === 'undefined') {
        const errMsg = document.getElementById('error-msg');
        errMsg.textContent = 'Failed to load Three.js. Check internet connection.';
        errMsg.style.display = 'block';
        console.error('Three.js failed to load');
        return;
    }

    setupScene();
    attachEventListeners();
    await updateCube();
    console.log('CubeForge ready');
}

if (document.readyState === 'complete') {
    init();
} else {
    window.addEventListener('load', init);
}
