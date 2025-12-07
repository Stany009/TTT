// Register service worker for PWA functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('ServiceWorker registered successfully');
            })
            .catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('.cell');
    const statusEl = document.getElementById('status');
    const resetBtn = document.getElementById('reset-btn');
    const difficultySelect = document.getElementById('difficulty');
    const playerSymbolSelect = document.getElementById('player-symbol');

    let gameState = {};
    let soundsEnabled = false;

    // Enable sounds on first user interaction
    document.addEventListener('click', () => {
        if (!soundsEnabled) {
            gameSounds.enabled = true;
            soundsEnabled = true;
        }
    });

    // Load initial game state
    loadGameState();

    // Add event listeners
    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    resetBtn.addEventListener('click', resetGame);

    function loadGameState() {
        const difficulty = difficultySelect.value;
        const player_symbol = playerSymbolSelect.value;
        const data = gameState.board ? {
            board: gameState.board,
            state: gameState.state,
            difficulty,
            player_symbol
        } : { difficulty, player_symbol };
        
        fetch('/game_state', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            gameState = data;
            updateBoard();
            updateStatus();
        })
        .catch(error => console.error('Error loading game state:', error));
    }

    function updateBoard() {
        const previousLength = gameState.board ? gameState.board.filter(cell => cell !== ' ').length : 0;
        cells.forEach((cell, index) => {
            cell.textContent = gameState.board[index] === ' ' ? '' : gameState.board[index];
            cell.classList.toggle('taken', gameState.board[index] !== ' ');
        });
        const currentLength = gameState.board.filter(cell => cell !== ' ').length;
        if (currentLength > previousLength && currentLength % 2 === 0 && currentLength > 0) {
            gameSounds.playAIMove();
        }
    }

    function updateStatus() {
        const state = gameState.state;
        if (state === 'human_win') {
            statusEl.textContent = 'You win!';
            gameSounds.playWin();
        } else if (state === 'ai_win') {
            statusEl.textContent = 'AI wins!';
            gameSounds.playLoss();
        } else if (state === 'draw') {
            statusEl.textContent = 'It\'s a draw!';
            gameSounds.playDraw();
        } else {
            const currentPlayer = gameState.board.filter(cell => cell !== ' ').length % 2 === 0 ? 'Your turn' : 'AI\'s turn';
            const symbol = currentPlayer === 'Your turn' ? playerSymbolSelect.value : (playerSymbolSelect.value === 'X' ? 'O' : 'X');
            statusEl.textContent = `${currentPlayer} (${symbol})`;
        }
    }

    function handleCellClick(event) {
        const cellIndex = Array.from(cells).indexOf(event.target);
        if (gameState.board[cellIndex] !== ' ' || gameState.state !== 'ongoing') {
            return;
        }

        fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ position: cellIndex }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            gameSounds.playMove();
            gameState = data;
            updateBoard();
            updateStatus();
        })
        .catch(error => console.error('Error making move:', error));
    }

    function resetGame() {
        const difficulty = difficultySelect.value;
        const player_symbol = playerSymbolSelect.value;

        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ difficulty, player_symbol }),
        })
        .then(response => response.json())
        .then(data => {
            gameState = data;
            updateBoard();
            updateStatus();
        })
        .catch(error => console.error('Error resetting game:', error));
    }
});
