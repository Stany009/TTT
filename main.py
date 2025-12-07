from flask import Flask, render_template, request, jsonify, session
from game import TicTacToe
from ai import TicTacToeAI
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

def get_game():
    """Get the current game from session, or create a new one."""
    if 'game_board' not in session:
        game = TicTacToe()
        session['game_board'] = game.board
        session['player_symbol'] = game.human
        session['difficulty'] = 'hard'
    else:
        game = TicTacToe(session.get('player_symbol', 'X'))
        game.board = session['game_board']
    return game

def get_ai(game):
    """Get the AI for the current game."""
    difficulty = session.get('difficulty', 'hard')
    return TicTacToeAI(game, difficulty)

def save_game(game):
    """Save the game state to session."""
    session['game_board'] = game.board
    session['player_symbol'] = game.human
    session['difficulty'] = session.get('difficulty', 'hard')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def game_state():
    game = get_game()
    return jsonify(game.to_dict())

@app.route('/make_move', methods=['POST'])
def make_move():
    game = get_game()
    ai = get_ai(game)
    data = request.get_json()
    position = data.get('position')
    if position is None or not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({'error': 'Invalid position'}), 400
    if game.board[position] != ' ':
        return jsonify({'error': 'Position already taken'}), 400
    
    # Human move
    game.make_move(position, game.human)
    
    # Check if game over after human move
    if game.is_game_over():
        save_game(game)
        return jsonify(game.to_dict())
    
    # AI move
    ai_move = ai.get_best_move()
    game.make_move(ai_move, game.ai)
    
    save_game(game)
    return jsonify(game.to_dict())

@app.route('/reset', methods=['POST'])
def reset():
    data = request.get_json() or {}
    difficulty = data.get('difficulty', 'hard')
    player_symbol = data.get('player_symbol', 'X')
    game = TicTacToe(player_symbol)
    session['game_board'] = game.board
    session['player_symbol'] = player_symbol
    session['difficulty'] = difficulty
    return jsonify(game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
