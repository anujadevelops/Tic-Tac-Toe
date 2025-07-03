import tkinter as tk
from tkinter import filedialog
import random

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic Tac Toe")
        self.players = ["Player 1", "Player 2"]
        self.mode = "Single Player"
        self.rounds = 5
        self.current_round = 1
        self.score = {self.players[0]: 0, self.players[1]: 0}
        self.board = [""] * 9
        self.buttons = []
        self.current_player = self.players[0]
        self.ai_symbol = "O"
        self.human_symbol = "X"
        self.difficulty = "Hard"
        self.dark_mode = False

        self.root.configure(bg="#f0f8ff")
        self.create_setup_panel()

    def create_setup_panel(self):
        self.setup_frame = tk.Frame(self.root, bg="#f0f8ff", padx=20, pady=20)
        self.setup_frame.pack(pady=20)

        tk.Label(self.setup_frame, text="🎮 Welcome to Tic Tac Toe!", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.add_labeled_entry("player1_entry", "Player 1 Name:", "Player 1", 1)
        self.add_option_menu("game_var", "Game Mode:", ["Single Player", "Two Players"], 2, self.toggle_player2)
        self.add_labeled_entry("player2_entry", "Player 2 Name:", "Computer", 3)
        self.add_labeled_entry("rounds_entry", "Rounds:", "5", 4)
        self.add_option_menu("difficulty_var", "Difficulty:", ["Easy", "Medium", "Hard"], 5)

        tk.Button(self.setup_frame, text="Start Game", command=self.start_game,
                  bg="#4682b4", fg="white", font=("Arial", 12, "bold"), relief="raised",
                  padx=10, pady=5).grid(row=6, column=0, columnspan=2, pady=15)

    def add_labeled_entry(self, attr_name, label, default, row):
        tk.Label(self.setup_frame, text=label, bg="#f0f8ff", fg="#333").grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(self.setup_frame, font=("Arial", 12))
        entry.insert(0, default)
        entry.grid(row=row, column=1, pady=5)
        setattr(self, attr_name, entry)

    def add_option_menu(self, attr_name, label, options, row, command=None):
        tk.Label(self.setup_frame, text=label, bg="#f0f8ff", fg="#333").grid(row=row, column=0, sticky="w", pady=5)
        var = tk.StringVar(value=options[0])
        tk.OptionMenu(self.setup_frame, var, *options, command=command).grid(row=row, column=1, pady=5)
        setattr(self, attr_name, var)

    def toggle_player2(self, mode):
        if mode == "Single Player":
            self.player2_entry.delete(0, tk.END)
            self.player2_entry.insert(0, "Computer")
        else:
            self.player2_entry.delete(0, tk.END)
            self.player2_entry.insert(0, "Player 2")

    def start_game(self):
        self.players[0] = self.player1_entry.get()
        self.players[1] = self.player2_entry.get()
        self.mode = self.game_var.get()
        self.rounds = int(self.rounds_entry.get())
        self.difficulty = self.difficulty_var.get()
        self.score = {self.players[0]: 0, self.players[1]: 0}
        self.current_round = 1

        self.setup_frame.destroy()
        self.create_menu()
        self.create_scoreboard()
        self.create_board()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game Settings", command=self.open_settings_page)
        game_menu.add_command(label="View Current Scores", command=self.show_scores)
        game_menu.add_command(label="Reset Scores", command=self.reset_scores)
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_command(label="Save Scores", command=self.save_scores)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)

    def open_settings_page(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Game Settings")
        settings_window.grab_set()

        tk.Label(settings_window, text="Update Game Settings", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(settings_window, text="Player 1 Name:").pack()
        p1_entry = tk.Entry(settings_window)
        p1_entry.insert(0, self.players[0])
        p1_entry.pack()

        tk.Label(settings_window, text="Player 2 Name:").pack()
        p2_entry = tk.Entry(settings_window)
        p2_entry.insert(0, self.players[1])
        p2_entry.pack()

        tk.Label(settings_window, text="Game Mode:").pack()
        mode_var = tk.StringVar(value=self.mode)
        tk.OptionMenu(settings_window, mode_var, "Single Player", "Two Players").pack()

        tk.Label(settings_window, text="Difficulty:").pack()
        diff_var = tk.StringVar(value=self.difficulty)
        tk.OptionMenu(settings_window, diff_var, "Easy", "Medium", "Hard").pack()

        tk.Label(settings_window, text="Rounds:").pack()
        rounds_entry = tk.Entry(settings_window)
        rounds_entry.insert(0, str(self.rounds))
        rounds_entry.pack()

        def save_settings():
            self.players[0] = p1_entry.get()
            self.players[1] = p2_entry.get()
            self.mode = mode_var.get()
            self.difficulty = diff_var.get()
            self.rounds = int(rounds_entry.get())
            self.score = {self.players[0]: 0, self.players[1]: 0}
            self.current_round = 1
            self.update_scoreboard()
            self.reset_board()
            self.status_label.config(text="Settings updated. Game Reset.")
            settings_window.destroy()

        tk.Button(settings_window, text="Apply Settings", command=save_settings, bg="#4682b4", fg="white", padx=10, pady=5).pack(pady=10)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#1c1c1c" if self.dark_mode else "#f0f8ff"
        fg = "#e0e0e0" if self.dark_mode else "#333333"
        btn_bg = "#333333" if self.dark_mode else "#ffffff"

        self.root.configure(bg=bg)
        for btn in self.buttons:
            btn.configure(bg=btn_bg, fg=fg)

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg)
                for child in widget.winfo_children():
                    try:
                        child.configure(bg=bg, fg=fg)
                    except:
                        pass

    def create_scoreboard(self):
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        frame.pack(pady=10, padx=10)

        self.status_label = tk.Label(frame, text="Welcome to Tic Tac Toe!", font=("Arial", 14), bg="#ffffff")
        self.status_label.pack(pady=5)

        self.score_label = tk.Label(
            frame,
            text=f"{self.players[0]}: 0  |  {self.players[1]}: 0  |  Round: 1/{self.rounds}",
            font=("Arial", 12), bg="#ffffff")
        self.score_label.pack()

    def create_board(self):
        board_frame = tk.Frame(self.root, bg=self.root["bg"])
        board_frame.pack(pady=10)

        for i in range(9):
            btn = tk.Button(
                board_frame, text="", font=("Arial", 24), width=5, height=2,
                command=lambda idx=i: self.cell_clicked(idx),
                bg="#ffffff", relief="raised", bd=2
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    # Game Logic (AI, moves, end game)
    def cell_clicked(self, idx):
        if self.board[idx] == "" and self.current_round <= self.rounds:
            self.board[idx] = self.get_symbol()
            color = "#87cefa" if self.get_symbol() == self.human_symbol else "#f08080"
            self.buttons[idx].config(text=self.board[idx], bg=color)

            winner, win_line = self.check_winner()
            if winner or self.is_draw():
                self.animate_win(win_line) if win_line else None
                self.root.after(500, lambda: self.end_round(winner))
            else:
                self.switch_player()
                if self.mode == "Single Player" and self.current_player == self.players[1]:
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.difficulty == "Easy":
            empty = [i for i, val in enumerate(self.board) if val == ""]
            idx = random.choice(empty)
        elif self.difficulty == "Medium":
            idx = self.medium_ai_move()
        else:
            idx = self.minimax_ai_move()

        self.board[idx] = self.ai_symbol
        self.buttons[idx].config(text=self.ai_symbol, bg="#f08080")

        winner, win_line = self.check_winner()
        if winner or self.is_draw():
            self.animate_win(win_line) if win_line else None
            self.root.after(500, lambda: self.end_round(winner))
        else:
            self.switch_player()

    def medium_ai_move(self):
        for idx in range(9):
            if self.board[idx] == "":
                test_board = self.board.copy()
                test_board[idx] = self.ai_symbol
                if self.check_winner_on_board(test_board)[0]:
                    return idx
        for idx in range(9):
            if self.board[idx] == "":
                test_board = self.board.copy()
                test_board[idx] = self.human_symbol
                if self.check_winner_on_board(test_board)[0]:
                    return idx
        empty = [i for i, val in enumerate(self.board) if val == ""]
        return random.choice(empty)

    def minimax_ai_move(self):
        best_score = -float('inf')
        best_move = None
        for idx in range(9):
            if self.board[idx] == "":
                self.board[idx] = self.ai_symbol
                score = self.minimax(False)
                self.board[idx] = ""
                if score > best_score:
                    best_score = score
                    best_move = idx
        return best_move

    def minimax(self, is_maximizing):
        winner, _ = self.check_winner()
        if winner == self.ai_symbol:
            return 1
        elif winner == self.human_symbol:
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for idx in range(9):
                if self.board[idx] == "":
                    self.board[idx] = self.ai_symbol
                    score = self.minimax(False)
                    self.board[idx] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for idx in range(9):
                if self.board[idx] == "":
                    self.board[idx] = self.human_symbol
                    score = self.minimax(True)
                    self.board[idx] = ""
                    best_score = min(score, best_score)
            return best_score

    def animate_win(self, line):
        if not line:
            return
        colors = ["#90ee90", "#32cd32", "#228b22"]
        for i, idx in enumerate(line):
            self.root.after(150 * i, lambda i=idx, c=colors[i]: self.buttons[i].config(bg=c))

    def get_symbol(self):
        return self.human_symbol if self.current_player == self.players[0] else self.ai_symbol

    def switch_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        self.status_label.config(text=f"{self.current_player}'s Turn")

    def check_winner(self):
        return self.check_winner_on_board(self.board)

    def check_winner_on_board(self, board):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)]
        for a, b, c in lines:
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a], (a, b, c)
        return None, None

    def is_draw(self):
        return "" not in self.board and not self.check_winner()[0]

    def end_round(self, winner):
        if winner:
            name = self.players[0] if winner == self.human_symbol else self.players[1]
            self.score[name] += 1
            self.status_label.config(text=f"{name} wins Round {self.current_round}!")
        else:
            self.status_label.config(text=f"Round {self.current_round} is a Draw!")
        self.current_round += 1
        self.update_scoreboard()

        if self.current_round > self.rounds:
            self.end_game()
        else:
            self.root.after(1000, self.reset_board)

    def update_scoreboard(self):
        self.score_label.config(
            text=f"{self.players[0]}: {self.score[self.players[0]]}  |  {self.players[1]}: {self.score[self.players[1]]}  |  Round: {self.current_round}/{self.rounds}"
        )

    def reset_board(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg="#ffffff")
        self.current_player = self.players[0]
        self.status_label.config(text=f"{self.current_player}'s Turn")

    def end_game(self):
        winner = max(self.score, key=self.score.get)
        self.status_label.config(text=f"Game Over! {winner} wins the game! (Auto Reset Soon)")
        self.root.after(3000, self.reset_scores)

    def reset_scores(self):
        self.score = {self.players[0]: 0, self.players[1]: 0}
        self.current_round = 1
        self.update_scoreboard()
        self.reset_board()
        self.status_label.config(text="Scores reset. New Game Starts!")

    def save_scores(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(f"Tic Tac Toe Scores - {self.rounds} Rounds\n")
                file.write(f"{self.players[0]}: {self.score[self.players[0]]}\n")
                file.write(f"{self.players[1]}: {self.score[self.players[1]]}\n")

    def show_scores(self):
        self.status_label.config(text=f"Current Scores — {self.players[0]}: {self.score[self.players[0]]}, {self.players[1]}: {self.score[self.players[1]]}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
