const API_BASE = 'http://localhost:5000/api';

function listPlayers() {}

function showForm() {}

function startNewGame() {}

function showScoreForm() {}

function showScores() {}

function quitGame() {}


async function sendMove(direction) {
    await fetch(`${API_BASE}/move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction: direction })
    });
}

document.addEventListener('keydown', (event) => {
    const key = event.key;
    if (['ArrowUp', 'w', 'W'].includes(key)) sendMove('up');
    else if (['ArrowDown', 's', 'S'].includes(key)) sendMove('down');
    else if (['ArrowLeft', 'a', 'A'].includes(key)) sendMove('left');
    else if (['ArrowRight', 'd', 'D'].includes(key)) sendMove('right');
});