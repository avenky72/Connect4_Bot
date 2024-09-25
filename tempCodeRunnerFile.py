import tkinter as tk
import random

class ConnectFourGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.rows = 6
        self.columns = 7
        self.board = [[0] * self.columns for _ in range(self.rows)]
        self.current_turn = 1  # Player 1 starts
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        for col in range(self.columns):
            button = tk.Button(self.master, text='Drop', command=lambda c=col: self.drop_piece(c))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        self.status_label = tk.Label(self.master, text="Player 1's turn")
        self.status_label.grid(row=1, columnspan=self.columns)

        self.canvas = tk.Canvas(self.master, width=700, height=600, bg='blue')
        self.canvas.grid(row=2, columnspan=self.columns)

    def drop_piece(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_turn
                self.draw_board()
                if self.check_winner(self.current_turn):
                    self.status_label.config(text=f"Player {self.current_turn} wins!")
                    return
                self.current_turn = 2 if self.current_turn == 1 else 1
                self.status_label.config(text=f"Player {self.current_turn}'s turn")
                self.master.update()
                if self.current_turn == 2:  # AI's turn
                    self.ai_move()
                break

    def ai_move(self):
        move = self.choose_best_move(2)  # AI is player 2
        if move is not None:
            self.drop_piece(move)

    def choose_best_move(self, mark):
        valid_moves = [col for col in range(self.columns) if self.board[0][col] == 0]
        scores = {}
        
        for col in valid_moves:
            child = self.drop_piece_simulation(col, mark)
            score = self.minimax(child, 6, False, mark, -float('inf'), float('inf'))
            scores[col] = score

        # Check for immediate threats from the opponent and prioritize blocking
        for col in valid_moves:
            if self.is_threat(col, mark % 2 + 1):  # Check if opponent can win
                return col

        best_score = max(scores.values())
        best_moves = [col for col in scores if scores[col] == best_score]
        return random.choice(best_moves)

    def drop_piece_simulation(self, col, mark):
        sim_board = [row[:] for row in self.board]
        for row in range(self.rows - 1, -1, -1):
            if sim_board[row][col] == 0:
                sim_board[row][col] = mark
                break
        return sim_board

    def minimax(self, board, depth, maximizingPlayer, mark, alpha, beta):
        if self.check_winner(1):
            return -1000000  # Player 1 wins
        if self.check_winner(2):
            return 1000000  # AI wins
        if depth == 0 or all(board[0][col] != 0 for col in range(self.columns)):
            return self.evaluate_board(board, mark)

        if maximizingPlayer:
            max_eval = -float('inf')
            for col in range(self.columns):
                if board[0][col] == 0:
                    child = self.drop_piece_simulation(col, mark)
                    eval = self.minimax(child, depth - 1, False, mark, alpha, beta)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(self.columns):
                if board[0][col] == 0:
                    child = self.drop_piece_simulation(col, 1 if mark == 2 else 2)
                    eval = self.minimax(child, depth - 1, True, mark, alpha, beta)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return min_eval

    def is_threat(self, col, opponent_mark):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                temp_board = self.drop_piece_simulation(col, opponent_mark)
                if self.check_winner(opponent_mark):
                    return True
                break
        return False

    def evaluate_board(self, board, mark):
        score = 0
        opponent = 1 if mark == 2 else 2
        
        for row in range(self.rows):
            for col in range(self.columns):
                if board[row][col] == mark:
                    score += self.get_position_score(row, col, mark)
                elif board[row][col] == opponent:
                    score -= self.get_position_score(row, col, opponent)

        return score

    def get_position_score(self, row, col, mark):
        # Basic scoring based on position
        score = 0
        center_column = self.columns // 2
        if col == center_column:
            score += 3
        elif col in (center_column - 1, center_column + 1):
            score += 2
        elif col in (center_column - 2, center_column + 2):
            score += 1

        return score

    def check_winner(self, mark):
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row][col + i] == mark for i in range(4)):
                    return True
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == mark for i in range(4)):
                    return True
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == mark for i in range(4)):
                    return True
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == mark for i in range(4)):
                    return True
        return False

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.columns):
                color = 'yellow' if self.board[row][col] == 1 else ('red' if self.board[row][col] == 2 else 'blue')
                x1 = col * 100 + 10
                y1 = row * 100 + 10
                x2 = x1 + 80
                y2 = y1 + 80
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline='black')

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFourGame(root)
    root.mainloop()
