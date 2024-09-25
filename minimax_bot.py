import tkinter as tk
import random

class ConnectFourGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.rows = 6
        self.columns = 7
        self.board = [[0] * self.columns for _ in range(self.rows)]
        self.current_turn = 1  
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
                if self.current_turn == 2: 
                    self.ai_move()
                break


    def ai_move(self):
        move = self.choose_best_move(2)  
        if move is not None:
            self.drop_piece(move)


    def choose_best_move(self, mark):
        valid_moves = [col for col in range(self.columns) if self.board[0][col] == 0]
        opponent = 1 if mark == 2 else 2
        for col in valid_moves:
            if self.is_winning_move(col, mark):
                return col
        for col in valid_moves:
            if self.is_winning_move(col, opponent):
                return col  
        best_score = -float('inf')
        best_move = random.choice(valid_moves)  
        for col in valid_moves:
            child = self.drop_piece_simulation(col, mark)
            score = self.minimax(child, 6, False, mark, -float('inf'), float('inf')) 
            if score > best_score:
                best_score = score
                best_move = col

        return best_move


    def drop_piece_simulation(self, col, mark):
        sim_board = [row[:] for row in self.board]
        for row in range(self.rows - 1, -1, -1):
            if sim_board[row][col] == 0:
                sim_board[row][col] = mark
                break
        return sim_board


    def minimax(self, board, depth, maximizingPlayer, mark, alpha, beta):
        if self.check_winner(1):
            return -1000000  
        if self.check_winner(2):
            return 1000000 
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

    def evaluate_board(self, board, mark):
        score = 0
        opponent = 1 if mark == 2 else 2

        for row in range(self.rows):
            for col in range(self.columns):
                if board[row][col] == mark:
                    score += self.get_position_score(row, col, mark)
                    score += self.score_window(board, row, col, mark)
                elif board[row][col] == opponent:
                    score -= self.score_window(board, row, col, opponent)

        return score

    def get_position_score(self, row, col, mark):
        score = 0
        center_column = self.columns // 2
        if col == center_column:
            score += 3
        elif col in (center_column - 1, center_column + 1):
            score += 2
        elif col in (center_column - 2, center_column + 2):
            score += 1

        return score

    def score_window(self, board, row, col, mark):
        score = 0
        opponent = 1 if mark == 2 else 2


        def count_consecutive_pieces(r_offset, c_offset):
            count = 0
            for i in range(4):
                r, c = row + i * r_offset, col + i * c_offset
                if 0 <= r < self.rows and 0 <= c < self.columns:
                    if board[r][c] == mark:
                        count += 1
                    elif board[r][c] == opponent:
                        return 0
            return count

        # Check horizontal, vertical, and diagonal patterns
        score += count_consecutive_pieces(0, 1)  # Horizontal
        score += count_consecutive_pieces(1, 0)  # Vertical
        score += count_consecutive_pieces(1, 1)  # Diagonal /
        score += count_consecutive_pieces(1, -1) # Diagonal \

        return score


    def is_winning_move(self, col, mark):
        """Check if dropping a piece in this column will result in a win."""
        temp_board = self.drop_piece_simulation(col, mark)
        return self.check_winner_on_board(temp_board, mark)


    def check_winner_on_board(self, board, mark):
        """Check if a specific player has won on a given board."""
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(board[row][col + i] == mark for i in range(4)):
                    return True
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if all(board[row + i][col] == mark for i in range(4)):
                    return True
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(board[row - i][col + i] == mark for i in range(4)):
                    return True
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(board[row + i][col + i] == mark for i in range(4)):
                    return True
        return False


    def check_winner(self, mark):
        return self.check_winner_on_board(self.board, mark)


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
