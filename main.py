# version1_basic.py
import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeApp:
    """Basic Tic-Tac-Toe Application - Phase 1"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")
        
        # Game state
        self.board = [""] * 9
        self.current_player = "X"  # X always goes first
        self.game_over = False
        
        # Track wins for simple stats
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        
        # Font definitions
        self.title_font = ('Helvetica', 20, 'bold')
        self.board_font = ('Helvetica', 32, 'bold')
        self.button_font = ('Helvetica', 12)
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create the game interface widgets."""
        # Title
        self.title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=self.title_font,
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=20)
        
        # Turn indicator
        self.turn_label = tk.Label(
            self.root,
            text="Player X's turn",
            font=('Helvetica', 14),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.turn_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.board_frame.pack(pady=20)
        
        # Create board buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=self.board_font,
                width=3,
                height=1,
                bg="#ecf0f1",
                fg="#2c3e50",
                relief='raised',
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, ipadx=10, ipady=10)
            self.buttons.append(btn)
        
        # Score display
        self.score_label = tk.Label(
            self.root,
            text="X: 0  |  O: 0  |  Draws: 0",
            font=('Helvetica', 12),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.score_label.pack(pady=10)
        
        # Control buttons
        self.control_frame = tk.Frame(self.root, bg="#2c3e50")
        self.control_frame.pack(pady=10)
        
        self.reset_btn = tk.Button(
            self.control_frame,
            text="New Game",
            font=self.button_font,
            bg="#3498db",
            fg="white",
            command=self.reset_game
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.quit_btn = tk.Button(
            self.control_frame,
            text="Quit",
            font=self.button_font,
            bg="#e74c3c",
            fg="white",
            command=self.root.quit
        )
        self.quit_btn.pack(side=tk.LEFT, padx=5)
    
    def make_move(self, index: int):
        """Handle a player's move."""
        if self.game_over or self.board[index] != "":
            return
        
        # Make the move
        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            fg="#e74c3c" if self.current_player == "X" else "#2ecc71"
        )
        
        # Check win
        if self.check_win():
            self.game_over = True
            if self.current_player == "X":
                self.x_wins += 1
            else:
                self.o_wins += 1
            self.update_score()
            self.highlight_winning_line()
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            return
        
        # Check draw
        if all(cell != "" for cell in self.board):
            self.game_over = True
            self.draws += 1
            self.update_score()
            messagebox.showinfo("Game Over", "It's a draw!")
            return
        
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_turn_label()
    
    def check_win(self) -> bool:
        """Check if current player has won."""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for pattern in win_patterns:
            if all(self.board[i] == self.current_player for i in pattern):
                self.winning_line = pattern
                return True
        return False
    
    def highlight_winning_line(self):
        """Highlight the winning line."""
        if hasattr(self, 'winning_line'):
            for i in self.winning_line:
                self.buttons[i].config(bg="#f1c40f")
    
    def update_turn_label(self):
        """Update the turn indicator."""
        color = "#e74c3c" if self.current_player == "X" else "#2ecc71"
        self.turn_label.config(
            text=f"Player {self.current_player}'s turn",
            fg=color
        )
    
    def update_score(self):
        """Update the score display."""
        self.score_label.config(
            text=f"X: {self.x_wins}  |  O: {self.o_wins}  |  Draws: {self.draws}"
        )
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winning_line = None
        
        for btn in self.buttons:
            btn.config(text="", bg="#ecf0f1")
        
        self.update_turn_label()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()