import tkinter as tk
import math

# Minimax logic
def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
                      (0, 4, 8), (2, 4, 6)]             # Diagonal
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def available_moves(board):
    return [i for i, x in enumerate(board) if x == ' ']

def is_board_full(board):
    return ' ' not in board

def minimax(board, depth, is_maximizing, ai_player, human_player):
    if check_winner(board, ai_player):
        return 1
    elif check_winner(board, human_player):
        return -1
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = ai_player
            score = minimax(board, depth + 1, False, ai_player, human_player)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = human_player
            score = minimax(board, depth + 1, True, ai_player, human_player)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def ai_move(board, ai_player, human_player):
    best_score = -math.inf
    move = None
    for potential_move in available_moves(board):
        board[potential_move] = ai_player
        score = minimax(board, 0, False, ai_player, human_player)
        board[potential_move] = ' '
        if score > best_score:
            best_score = score
            move = potential_move
    board[move] = ai_player

# GUI logic
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_player = 'X'  # Human player starts
        self.buttons = []
        self.ai_player = 'O'
        self.human_player = 'X'
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            button = tk.Button(frame, text=' ', width=10, height=3, font=('Arial', 24),
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        self.reset_button = tk.Button(self.root, text="Reset", font=('Arial', 14), command=self.reset_game)
        self.reset_button.pack(pady=20)

    def on_button_click(self, index):
        if self.board[index] == ' ' and self.current_player == self.human_player:
            self.board[index] = self.human_player
            self.buttons[index].config(text=self.human_player)

            if check_winner(self.board, self.human_player):
                self.display_winner("You win!")
                return
            elif is_board_full(self.board):
                self.display_winner("It's a tie!")
                return

            self.current_player = self.ai_player
            self.ai_turn()

    def ai_turn(self):
        ai_move(self.board, self.ai_player, self.human_player)
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

        if check_winner(self.board, self.ai_player):
            self.display_winner("AI wins!")
        elif is_board_full(self.board):
            self.display_winner("It's a tie!")
        else:
            self.current_player = self.human_player

    def display_winner(self, winner_message):
        for button in self.buttons:
            button.config(state='disabled')
        winner_label = tk.Label(self.root, text=winner_message, font=('Arial', 24))
        winner_label.pack(pady=20)

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = self.human_player
        for button in self.buttons:
            button.config(text=' ', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
