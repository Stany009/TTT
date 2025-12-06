from game import TicTacToe
import random

class TicTacToeAI:
    """AI player using the Minimax algorithm with difficulty levels."""
    
    def __init__(self, game, difficulty='hard'):
        """Initialize the AI with a game reference and difficulty level."""
        self.game = game
        self.player = game.ai
        self.opponent = game.human
        self.difficulty = difficulty
        self.max_depth = {'easy': 1, 'medium': 3, 'hard': 9}[difficulty]
    
    def minimax(self, is_maximizing, depth=0):
        """
        Minimax algorithm to find the best move with depth limit for difficulty.
        
        Args:
            is_maximizing: Boolean indicating if we're maximizing (AI turn) or minimizing (human turn)
            depth: Current depth in the game tree
        
        Returns:
            The score of the position
        """
        # Check terminal states
        if self.game.is_winner(self.player):
            return 10 - depth  # AI wins (reward decreases with depth to find faster wins)
        elif self.game.is_winner(self.opponent):
            return depth - 10  # Human wins (penalty increases with depth to delay losses)
        elif self.game.is_board_full():
            return 0  # Draw
        
        # Depth limit for difficulty
        if depth >= self.max_depth:
            return 0  # Neutral score at max depth
        
        if is_maximizing:
            # AI's turn - maximize score
            max_score = float('-inf')
            for move in self.game.get_available_moves():
                self.game.make_move(move, self.player)
                score = self.minimax(False, depth + 1)
                self.game.undo_move(move)
                max_score = max(score, max_score)
            return max_score
        else:
            # Human's turn - minimize score
            min_score = float('inf')
            for move in self.game.get_available_moves():
                self.game.make_move(move, self.opponent)
                score = self.minimax(True, depth + 1)
                self.game.undo_move(move)
                min_score = min(score, min_score)
            return min_score
    
    def get_best_move(self):
        """
        Determine the best move for the AI using Minimax.
        
        Returns:
            The position (0-8) of the best move
        """
        best_score = float('-inf')
        best_move = None
        
        for move in self.game.get_available_moves():
            self.game.make_move(move, self.player)
            score = self.minimax(False)  # After AI moves, it's human's turn (minimizing)
            self.game.undo_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
