const API_BASE = 'http://127.0.0.1:5000/api';

function listPlayers() {
    fetch(`${API_BASE}/players`)
    .then(response => response.json())
    .then(data => {
        const output = document.getElementById('output');
        output.innerHTML = '<h2>Players</h2>';
        output.innerHTML += '<ul>';
        data.players.forEach(player => {
            output.innerHTML += `<li>${player.name} | Total Score: ${player.total_score} | Last Session: ${player.last_session_time}</li>`;
        });
        output.innerHTML += '</ul>';
    });
}

async function fetchGameState() {
    const response = await fetch(`${API_BASE}/game/state`);
    if (response.ok) {
        const gameState = await response.json();
        updateGrid(gameState);
        document.getElementById('score').textContent = `Score: ${gameState.cat.score || 0}`;
        document.getElementById('berries').textContent = `Berries Collected: ${gameState.cat.berries_collected} / ${gameState.cat.berries_required}`;    
    } 
}

function generateGrid() {
    const gameContainer = document.getElementById('game-container');
    gameContainer.innerHTML = '';
    for (let y = 0; y < 10; y++) {
        for (let x = 0; x < 10; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.x = x;
            cell.dataset.y = y;
            gameContainer.appendChild(cell);
        }
    }
}

function savePlayer(){
    fetch(`${API_BASE}/save_score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => {
        if (response.ok) {
            alert('Game saved!');
        }
    });
}

function updateGrid(gameState) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.style.backgroundImage = '';
    });

    const catX = gameState.cat.x;
    const catY = gameState.cat.y;

    gameState.berries.forEach(berry => {
        const berryCell = document.querySelector(`.cell[data-x="${berry.x}"][data-y="${berry.y}"]`);
        if (berryCell) {
            berryCell.style.backgroundImage = 'url("assets/berry.png")';
            berryCell.style.backgroundSize = 'cover';
        }
    });

    const catCell = document.querySelector(`.cell[data-x="${catX}"][data-y="${catY}"]`);
    if (catCell) {
        catCell.style.backgroundImage = 'url("assets/cat.png")'; 
        catCell.style.backgroundSize = 'cover';
    }



    if (gameState.cat.berries_collected >= gameState.cat.berries_required) {
        document.getElementById('game-over').style.display = 'block';
        savePlayer();
    } else {
        document.getElementById('game-over').style.display = 'none';
    }
}


function startNewGame() {
    const playerName = document.getElementById('player-name').value;
    fetch(`${API_BASE}/start_game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_name: playerName })
    }).then(response => {
        if (response.ok) {
            fetchGameState();
            alert('Game started!');
        }
    });
}



function showScores() {
    const playerName = document.getElementById('player-name').value;
    fetch(`${API_BASE}/scores/${playerName}`)
        .then(response => response.json())
        .then(data => {
            const output = document.getElementById('output');
            if (data.exists) {
                output.innerHTML = `<h2>Scores of ${playerName}</h2>`;
                output.innerHTML += '<ul>';
                data.scores.forEach(score => {
                    output.innerHTML += `<li>Score: ${score.score} | Berries: ${score.collected_berries}</li>`;
                });
                output.innerHTML += '</ul>';
            } else {
                output.innerHTML = `<p>Player ${playerName} not found.</p>`;
            }
        });
}


async function sendMove(direction) {
    await fetch(`${API_BASE}/move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction: direction })
    });

    await fetchGameState();
}

document.addEventListener('keydown', (event) => {
    const key = event.key;
    if (['ArrowUp', 'w', 'W'].includes(key)) sendMove('up');
    else if (['ArrowDown', 's', 'S'].includes(key)) sendMove('down');
    else if (['ArrowLeft', 'a', 'A'].includes(key)) sendMove('left');
    else if (['ArrowRight', 'd', 'D'].includes(key)) sendMove('right'); 
});

document.addEventListener('DOMContentLoaded', () => {
    generateGrid();
});