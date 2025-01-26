# version2_enhanced.py
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

class TicTacToeApp:
    """Enhanced Tic-Tac-Toe Application - Phase 2"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe - Enhanced")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        
        # Game statistics
        self.stats_file = "tictactoe_stats.json"
        self.stats = self.load_stats()
        
        # Font definitions
        self.fonts = {
            'title': ('Helvetica', 24, 'bold'),
            'header': ('Helvetica', 14, 'bold'),
            'button': ('Helvetica', 12),
            'board': ('Helvetica', 30, 'bold')
        }
        
        self.create_main_menu()
    
    def load_stats(self) -> dict:
        """Load game statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'pvp_wins': {'Player 1': 0, 'Player 2': 0},
            'pvp_draws': 0,
            'ai_wins': {'Player': 0, 'AI': 0},
            'ai_draws': 0,
            'total_games': 0
        }
    
    def save_stats(self):
        """Save game statistics to file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def create_main_menu(self):
        """Create the main menu interface."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        tk.Label(
            self.root,
            text="Tic-Tac-Toe\nEnhanced Edition",
            font=self.fonts['title'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=30)
        
        # Menu buttons
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        buttons = [
            ("Player vs Player", self.start_pvp_game),
            ("Player vs AI", self.start_ai_menu),
            ("Game Statistics", self.show_stats),
            ("Quit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.fonts['button'],
                bg="#3498db",
                fg="white",
                padx=20,
                pady=8,
                width=20,
                command=command
            )
            btn.pack(pady=8)
    
    def start_pvp_game(self):
        """Start a player vs player game."""
        game_window = tk.Toplevel(self.root)
        game_window.title("Player vs Player")
        game_window.geometry("500x600")
        TicTacToeGame(game_window, mode="pvp", app=self)
    
    def start_ai_menu(self):
        """Show AI difficulty selection menu."""
        ai_menu = tk.Toplevel(self.root)
        ai_menu.title("Select AI Difficulty")
        ai_menu.geometry("400x300")
        ai_menu.configure(bg="#2c3e50")
        
        tk.Label(
            ai_menu,
            text="Select AI Difficulty",
            font=self.fonts['title'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=20)
        
        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard")
        ]
        
        for text, difficulty in difficulties:
            btn = tk.Button(
                ai_menu,
                text=text,
                font=self.fonts['button'],
                bg="#3498db",
                fg="white",
                command=lambda d=difficulty: self.start_ai_game(d, ai_menu)
            )
            btn.pack(pady=8, ipadx=10)
        
        ai_menu.grab_set()
    
    def start_ai_game(self, difficulty: str, menu_window: tk.Toplevel):
        """Start a player vs AI game."""
        menu_window.destroy()
        game_window = tk.Toplevel(self.root)
        game_window.title(f"Player vs AI ({difficulty.capitalize()})")
        game_window.geometry("500x600")
        TicTacToeGame(game_window, mode="ai", app=self, ai_difficulty=difficulty)
    
    def show_stats(self):
        """Show game statistics."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")
        stats_window.geometry("450x400")
        stats_window.configure(bg="#2c3e50")
        
        tk.Label(
            stats_window,
            text="Game Statistics",
            font=self.fonts['title'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=15)
        
        # Player vs Player stats
        pvp_frame = tk.Frame(stats_window, bg="#2c3e50")
        pvp_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            pvp_frame,
            text="Player vs Player:",
            font=self.fonts['header'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        for player, wins in self.stats['pvp_wins'].items():
            tk.Label(
                pvp_frame,
                text=f"{player}: {wins} wins",
                font=self.fonts['button'],
                bg="#2c3e50",
                fg="#ecf0f1"
            ).pack(anchor=tk.W)
        
        tk.Label(
            pvp_frame,
            text=f"Draws: {self.stats['pvp_draws']}",
            font=self.fonts['button'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        # Player vs AI stats
        ai_frame = tk.Frame(stats_window, bg="#2c3e50")
        ai_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            ai_frame,
            text="Player vs AI:",
            font=self.fonts['header'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        for player, wins in self.stats['ai_wins'].items():
            tk.Label(
                ai_frame,
                text=f"{player}: {wins} wins",
                font=self.fonts['button'],
                bg="#2c3e50",
                fg="#ecf0f1"
            ).pack(anchor=tk.W)
        
        tk.Label(
            ai_frame,
            text=f"Draws: {self.stats['ai_draws']}",
            font=self.fonts['button'],
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        # Total games
        tk.Label(
            stats_window,
            text=f"Total games: {self.stats['total_games']}",
            font=self.fonts['header'],
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=10
        ).pack()
        
        close_btn = tk.Button(
            stats_window,
            text="Close",
            font=self.fonts['button'],
            bg="#e74c3c",
            fg="white",
            command=stats_window.destroy
        )
        close_btn.pack(pady=10)


class TicTacToeGame:
    """Enhanced Tic-Tac-Toe game implementation."""
    
    def __init__(self, root: tk.Toplevel, mode: str, app: TicTacToeApp, ai_difficulty: str = "easy"):
        self.root = root
        self.mode = mode
        self.app = app
        self.ai_difficulty = ai_difficulty
        
        self.root.configure(bg="#2c3e50")
        
        # Game state
        self.board = [""] * 9
        self.current_player = 0  # 0 for Player 1/X, 1 for Player 2/O or AI
        self.game_over = False
        self.winning_line = None
        
        # Player configuration
        self.players = [
            {"name": "Player 1", "symbol": "X", "score": 0},
            {"name": "AI" if mode == "ai" else "Player 2", "symbol": "O", "score": 0}
        ]
        
        # Create UI
        self.create_widgets()
        
        # If AI's turn first
        if self.mode == "ai" and self.current_player == 1:
            self.root.after(500, self.ai_move)
    
    def create_widgets(self):
        """Create the game interface widgets."""
        # Header with score
        self.header_frame = tk.Frame(self.root, bg="#2c3e50")
        self.header_frame.pack(fill=tk.X, pady=10)
        
        self.score_label = tk.Label(
            self.header_frame,
            text=f"{self.players[0]['name']}: {self.players[0]['score']}  |  {self.players[1]['name']}: {self.players[1]['score']}",
            font=self.app.fonts['header'],
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.score_label.pack()
        
        # Turn indicator
        self.turn_label = tk.Label(
            self.root,
            text=f"{self.players[0]['name']}'s turn (X)",
            font=self.app.fonts['header'],
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.turn_label.pack(pady=5)
        
        # Difficulty indicator
        if self.mode == "ai":
            self.difficulty_label = tk.Label(
                self.root,
                text=f"AI Difficulty: {self.ai_difficulty.capitalize()}",
                font=self.app.fonts['button'],
                bg="#2c3e50",
                fg="#ecf0f1"
            )
            self.difficulty_label.pack()
        
        # Game board
        self.board_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.board_frame.pack(pady=20)
        
        # Create board buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=self.app.fonts['board'],
                width=3,
                height=1,
                bg="#ecf0f1",
                fg="#2c3e50",
                relief='raised',
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, ipadx=10, ipady=10)
            self.buttons.append(btn)
        
        # Control buttons
        self.control_frame = tk.Frame(self.root, bg="#2c3e50")
        self.control_frame.pack(pady=10)
        
        self.reset_btn = tk.Button(
            self.control_frame,
            text="New Game",
            font=self.app.fonts['button'],
            bg="#3498db",
            fg="white",
            command=self.reset_game
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.menu_btn = tk.Button(
            self.control_frame,
            text="Main Menu",
            font=self.app.fonts['button'],
            bg="#e74c3c",
            fg="white",
            command=self.return_to_menu
        )
        self.menu_btn.pack(side=tk.LEFT, padx=5)
    
    def make_move(self, index: int):
        """Handle a player's move."""
        if self.game_over or self.board[index] != "":
            return
        
        if self.mode == "ai" and self.current_player == 1:
            return  # Prevent player from making AI's move
        
        # Make the move
        self.update_board(index)
        
        # If in AI mode and game isn't over, let AI make a move
        if self.mode == "ai" and not self.game_over and self.current_player == 1:
            self.root.after(500, self.ai_move)
    
    def update_board(self, index: int):
        """Update the game board with a move."""
        player = self.players[self.current_player]
        self.board[index] = player["symbol"]
        
        # Update button
        color = "#e74c3c" if player["symbol"] == "X" else "#2ecc71"
        self.buttons[index].config(text=player["symbol"], fg=color)
        
        # Check game state
        if self.check_win():
            self.handle_win()
        elif self.check_draw():
            self.handle_draw()
        else:
            self.switch_player()
    
    def check_win(self) -> bool:
        """Check if current player has won."""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        symbol = self.players[self.current_player]["symbol"]
        for pattern in win_patterns:
            if all(self.board[i] == symbol for i in pattern):
                self.winning_line = pattern
                return True
        return False
    
    def handle_win(self):
        """Handle a win condition."""
        self.game_over = True
        player = self.players[self.current_player]
        player["score"] += 1
        
        # Highlight winning line
        self.highlight_winning_line()
        
        # Update score
        self.score_label.config(
            text=f"{self.players[0]['name']}: {self.players[0]['score']}  |  {self.players[1]['name']}: {self.players[1]['score']}"
        )
        
        # Disable buttons
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        # Update statistics
        winner_name = player["name"]
        if self.mode == "pvp":
            self.app.stats['pvp_wins'][winner_name] += 1
        else:
            self.app.stats['ai_wins'][winner_name] += 1
        self.app.stats['total_games'] += 1
        self.app.save_stats()
        
        messagebox.showinfo("Game Over", f"{player['name']} wins!", parent=self.root)
    
    def highlight_winning_line(self):
        """Highlight the winning line."""
        if self.winning_line:
            for i in self.winning_line:
                self.buttons[i].config(bg="#f1c40f")
    
    def check_draw(self) -> bool:
        """Check if the game is a draw."""
        return all(cell != "" for cell in self.board) and not self.winning_line
    
    def handle_draw(self):
        """Handle a draw condition."""
        self.game_over = True
        
        # Update statistics
        if self.mode == "pvp":
            self.app.stats['pvp_draws'] += 1
        else:
            self.app.stats['ai_draws'] += 1
        self.app.stats['total_games'] += 1
        self.app.save_stats()
        
        messagebox.showinfo("Game Over", "The game is a draw!", parent=self.root)
    
    def switch_player(self):
        """Switch to the next player."""
        self.current_player = 1 - self.current_player
        player = self.players[self.current_player]
        
        color = "#e74c3c" if player["symbol"] == "X" else "#2ecc71"
        self.turn_label.config(
            text=f"{player['name']}'s turn ({player['symbol']})",
            fg=color
        )
    
    def ai_move(self):
        """Make a move for the AI player."""
        if self.game_over:
            return
        
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if not empty_cells:
            return
        
        if self.ai_difficulty == "easy":
            # Random moves
            move = random.choice(empty_cells)
        elif self.ai_difficulty == "medium":
            # Smart move 50% of the time
            if random.random() < 0.5:
                move = self.find_smart_move()
            else:
                move = random.choice(empty_cells)
        else:  # hard
            # Always smart moves
            move = self.find_smart_move()
        
        self.update_board(move)
    
    def find_smart_move(self) -> int:
        """Find a smart move (win if possible, block if needed)."""
        # Check for winning move
        for i in [i for i, cell in enumerate(self.board) if cell == ""]:
            self.board[i] = self.players[1]["symbol"]
            if self.check_win():
                self.board[i] = ""
                return i
            self.board[i] = ""
        
        # Check for blocking move
        for i in [i for i, cell in enumerate(self.board) if cell == ""]:
            self.board[i] = self.players[0]["symbol"]
            # Temporarily switch to player to check win
            original_player = self.current_player
            self.current_player = 0
            if self.check_win():
                self.board[i] = ""
                self.current_player = original_player
                return i
            self.current_player = original_player
            self.board[i] = ""
        
        # Otherwise random
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_cells)
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = [""] * 9
        self.current_player = 0
        self.game_over = False
        self.winning_line = None
        
        # Reset buttons
        for btn in self.buttons:
            btn.config(text="", bg="#ecf0f1", state=tk.NORMAL)
        
        # Reset turn display
        player = self.players[0]
        self.turn_label.config(
            text=f"{player['name']}'s turn (X)",
            fg="#e74c3c"
        )
        
        # If AI's turn first
        if self.mode == "ai" and self.current_player == 1:
            self.root.after(500, self.ai_move)
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()