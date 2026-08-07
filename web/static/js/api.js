// Thin wrappers around the Flask REST API in app.py. Nothing here knows
// about Three.js or the DOM - it only speaks JSON in, JSON out.

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
            body: JSON.stringify({ move }),
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
            body: JSON.stringify({ notation }),
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
            body: JSON.stringify({ length: 20 }),
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
