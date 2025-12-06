from flask import Flask, render_template, request, jsonify
from game import TicTacToe
from ai import TicTacToeAI
import time

app = Flask(__name__)

# Global game instance
game = TicTacToe()
ai = TicTacToeAI(game)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def game_state():
    return jsonify(game.to_dict())

@app.route('/make_move', methods=['POST'])
def make_move():
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
        return jsonify(game.to_dict())
    
    # AI move
    ai_move = ai.get_best_move()
    game.make_move(ai_move, game.ai)
    
    return jsonify(game.to_dict())

@app.route('/reset', methods=['POST'])
def reset():
    global game, ai
    data = request.get_json() or {}
    difficulty = data.get('difficulty', 'hard')
    player_symbol = data.get('player_symbol', 'X')
    game = TicTacToe(player_symbol)
    ai = TicTacToeAI(game, difficulty)
    return jsonify(game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
