class TicTacToe:
    """Represents the Tic-Tac-Toe game board and logic."""
    
    def __init__(self, player_symbol='X'):
        """Initialize an empty board."""
        self.board = [' ' for _ in range(9)]
        self.human = player_symbol
        self.ai = 'O' if player_symbol == 'X' else 'X'
    
    def print_board(self):
        """Display the current board state."""
        print('\n')
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print('\n')
    
    def print_board_nums(self):
        """Display board with position numbers for reference."""
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        print('\nPosition Numbers:')
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
        print()
    
    def is_winner(self, player):
        """Check if the specified player has won."""
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in win_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def is_board_full(self):
        """Check if the board is full."""
        return ' ' not in self.board
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.is_winner(self.human) or self.is_winner(self.ai) or self.is_board_full()
    
    def get_available_moves(self):
        """Return a list of available move positions."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def make_move(self, position, player):
        """Place a player's mark on the board."""
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False
    
    def undo_move(self, position):
        """Remove a player's mark from the board."""
        self.board[position] = ' '
    
    def get_game_state(self):
        """Return the current game state: 'human_win', 'ai_win', 'draw', or 'ongoing'."""
        if self.is_winner(self.human):
            return 'human_win'
        elif self.is_winner(self.ai):
            return 'ai_win'
        elif self.is_board_full():
            return 'draw'
        else:
            return 'ongoing'
    
    def to_dict(self):
        """Return game state as dictionary for JSON serialization."""
        return {
            'board': self.board,
            'state': self.get_game_state()
        }
