const API_BASE = 'http://127.0.0.1:5000/api';
const MIN_SIZE = 5;
const MAX_SIZE = 25;
let currentSize = 10;

let gameIntervalId = null;
let lastDirection = null;
let gameOver = false;

function listPlayers() {
    fetch(`${API_BASE}/players`)
    .then(response => response.json())
    .then(data => {
        const output = document.getElementById('output');
        output.innerHTML = '<h2>Players</h2><ul>';
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

function generateGrid(size) {
    const gameContainer = document.getElementById('game-container');
    gameContainer.innerHTML = '';
    gameContainer.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    gameContainer.style.gridTemplateRows = `repeat(${size}, 1fr)`;
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.x = x;
            cell.dataset.y = y;
            gameContainer.appendChild(cell);
        }
    }
}

function savePlayer() {
    fetch(`${API_BASE}/save_score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => {
        if (response.ok) {
            gameOver = false;
            alert('Game saved!');
        }
    });
}

function updateGrid(gameState) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.style.backgroundImage = '';
    });

    if(!gameOver && gameState.game_over){
        document.getElementById('game-over').style.display = 'block';
        savePlayer();
        gameOver = true;
    }

    if(!gameOver){
        document.getElementById('game-over').style.display = 'none';
        
        gameState.berries.forEach(berry => {
            const berryCell = document.querySelector(`.cell[data-x="${berry.x}"][data-y="${berry.y}"]`);
            if (berryCell) {
                berryCell.style.backgroundImage = 'url("assets/berry.png")';
                berryCell.style.backgroundSize = 'cover';
            }
        });
        
        const catX = gameState.cat.x;
        const catY = gameState.cat.y;
        const catCell = document.querySelector(`.cell[data-x="${catX}"][data-y="${catY}"]`);
        if (catCell) {
            catCell.style.backgroundImage = 'url("assets/cat.png")';
            catCell.style.backgroundSize = 'cover';
        }

        gameState.cat.tail.forEach(t => {
            const tailCell = document.querySelector(`.cell[data-x="${t.x}"][data-y="${t.y}"]`);
            if (tailCell) {
                tailCell.style.backgroundImage = 'url("assets/tail.png")';
                tailCell.style.backgroundSize = 'cover';
            }
        });
    }
}

function startNewGame() {
    
    const playerName = document.getElementById('player-name').value.trim();
    if (!playerName) {
        alert('Please enter your name before starting.');
        return;
    }

    const boardSize = parseInt(document.getElementById('board-size').value, 10);
    if (isNaN(boardSize) || boardSize < MIN_SIZE || boardSize > MAX_SIZE) {
        alert(`Board size must be a number between ${MIN_SIZE} and ${MAX_SIZE}.`);
        return;
    }
    
    currentSize = boardSize;
    generateGrid(currentSize);

    fetch(`${API_BASE}/start_game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            player_name: playerName,
            board_size: currentSize
        })
    }).then(response => {
        if (response.ok) {
            if (gameIntervalId !== null) {
                clearInterval(gameIntervalId);
            }
            
            gameIntervalId = setInterval(fetchGameState, 100);
            fetchGameState();
        } else {
            alert('Failed to start new game. Please try again.');
        }
    });
}

async function sendMove(direction) {
    lastDirection = direction;
    await fetch(`${API_BASE}/move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ direction: direction })
    });
}

function showScores() {
    const playerName = document.getElementById('player-name').value.trim();
    if (!playerName) {
        alert('Please enter your name first.');
        return;
    }

    fetch(`${API_BASE}/scores/${playerName}`)
        .then(response => response.json())
        .then(data => {
            const output = document.getElementById('output');
            if (data.exists) {
                output.innerHTML = `<h2>Scores of ${playerName}</h2><ul>`;
                data.scores.forEach(score => {
                    output.innerHTML += `<li>Score: ${score.score} | Berries: ${score.collected_berries} | Board size: ${score.board_size}</li>`;
                });
                output.innerHTML += '</ul>';
            } else {
                output.innerHTML = `<p>Player ${playerName} not found.</p>`;
            }
        });
}

document.addEventListener('keydown', (event) => {
    const key = event.key;
    if (['ArrowUp', 'w', 'W'].includes(key)) sendMove('up');
    else if (['ArrowDown', 's', 'S'].includes(key)) sendMove('down');
    else if (['ArrowLeft', 'a', 'A'].includes(key)) sendMove('left');
    else if (['ArrowRight', 'd', 'D'].includes(key)) sendMove('right');
});

document.addEventListener('DOMContentLoaded', () => {
});
