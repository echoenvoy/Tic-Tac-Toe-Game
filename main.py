import tkinter as tk
from tkinter import font, messagebox, ttk
import json
import os
import time
from pygame import mixer
from typing import List, Optional, Dict, Tuple, Union
import random


class TicTacToeApp:
    """ Main application """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe Game")
        self.root.geometry("600x700")
        self.root.minsize(600, 700)
        self.root.configure(bg="#2c3e50")
        
        # Initialize sound mixer
        mixer.init()
        self.load_sounds()
        
        # Load game statistics
        self.stats_file = "tictactoe_stats.json"
        self.stats = self.load_stats()
        
        # Font definitions
        self.fonts = {
            'title': font.Font(family='Helvetica', size=28, weight='bold'),
            'header': font.Font(family='Helvetica', size=16, weight='bold'),
            'button': font.Font(family='Helvetica', size=14),
            'board': font.Font(family='Helvetica', size=36, weight='bold'),
            'stats': font.Font(family='Helvetica', size=12)
        }
        
        # Color scheme
        self.colors = {
            'bg': '#2c3e50',
            'primary': '#3498db',
            'secondary': '#2980b9',
            'accent': '#e74c3c',
            'text': '#ecf0f1',
            'board_bg': '#34495e',
            'grid': '#7f8c8d',
            'x': '#e74c3c',
            'o': '#2ecc71',
            'win': '#f1c40f',
            'timer': '#9b59b6'
        }
        
        self.create_main_menu()

    def load_sounds(self):
        """Load sound effects (using placeholder sounds - replace with actual files)."""
        self.sounds = {
            'move': None,
            'win': None,
            'draw': None,
            'click': None
        }
        try:
            # Replace these with actual sound files if available
            # self.sounds['move'] = mixer.Sound('move.wav')
            # self.sounds['win'] = mixer.Sound('win.wav')
            # self.sounds['draw'] = mixer.Sound('draw.wav')
            # self.sounds['click'] = mixer.Sound('click.wav')
            pass
        except:
            print("Sound files not found. Continuing without sound.")

    def play_sound(self, sound_name: str):
        """Play a sound effect if available."""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def load_stats(self) -> Dict:
        """Load game statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        # Default stats
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

    def update_stats(self, mode: str, winner: Optional[str]):
        """Update game statistics."""
        self.stats['total_games'] += 1
        
        if mode == "pvp":
            if winner:
                self.stats['pvp_wins'][winner] += 1
            else:
                self.stats['pvp_draws'] += 1
        else:  # ai mode
            if winner:
                self.stats['ai_wins'][winner] += 1
            else:
                self.stats['ai_draws'] += 1
        
        self.save_stats()

    def show_stats(self):
        """Show game statistics in a new window."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")
        stats_window.geometry("500x400")
        stats_window.configure(bg=self.colors['bg'])
        
        tk.Label(
            stats_window,
            text="Game Statistics",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        # Player vs Player stats
        pvp_frame = tk.Frame(stats_window, bg=self.colors['bg'])
        pvp_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            pvp_frame,
            text="Player vs Player:",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        for player, wins in self.stats['pvp_wins'].items():
            tk.Label(
                pvp_frame,
                text=f"{player}: {wins} wins",
                font=self.fonts['stats'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(anchor=tk.W)
        
        tk.Label(
            pvp_frame,
            text=f"Draws: {self.stats['pvp_draws']}",
            font=self.fonts['stats'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        # Player vs AI stats
        ai_frame = tk.Frame(stats_window, bg=self.colors['bg'])
        ai_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            ai_frame,
            text="Player vs AI:",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        for player, wins in self.stats['ai_wins'].items():
            tk.Label(
                ai_frame,
                text=f"{player}: {wins} wins",
                font=self.fonts['stats'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(anchor=tk.W)
        
        tk.Label(
            ai_frame,
            text=f"Draws: {self.stats['ai_draws']}",
            font=self.fonts['stats'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        # Total games
        tk.Label(
            stats_window,
            text=f"Total games played: {self.stats['total_games']}",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['text'],
            pady=10
        ).pack()
        
        close_btn = tk.Button(
            stats_window,
            text="Close",
            font=self.fonts['button'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=stats_window.destroy
        )
        close_btn.pack(pady=10)

    def create_main_menu(self):
        """Create the main menu interface."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="Tic-Tac-Toe Ultimate",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack()
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        # Menu buttons
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
                bg=self.colors['primary'],
                fg=self.colors['text'],
                activebackground=self.colors['secondary'],
                activeforeground=self.colors['text'],
                relief='flat',
                borderwidth=0,
                padx=20,
                pady=10,
                width=20,
                command=command
            )
            btn.pack(pady=10, ipadx=10, ipady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['secondary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['primary']))
            self.play_sound('click')
    
    def start_pvp_game(self):
        """Start a player vs player game."""
        game_window = tk.Toplevel(self.root)
        game_window.title("Player vs Player")
        game_window.geometry("550x700")
        TicTacToeGame(
            game_window, 
            mode="pvp", 
            colors=self.colors, 
            fonts=self.fonts, 
            stats=self.stats,
            play_sound=self.play_sound
        )
    
    def start_ai_menu(self):
        """Show AI difficulty selection menu."""
        ai_menu = tk.Toplevel(self.root)
        ai_menu.title("Select AI Difficulty")
        ai_menu.geometry("400x300")
        ai_menu.configure(bg=self.colors['bg'])
        
        tk.Label(
            ai_menu,
            text="Select AI Difficulty",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=20)
        
        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard"),
            ("Unbeatable", "unbeatable")
        ]
        
        for text, difficulty in difficulties:
            btn = tk.Button(
                ai_menu,
                text=text,
                font=self.fonts['button'],
                bg=self.colors['primary'],
                fg=self.colors['text'],
                command=lambda d=difficulty: self.start_ai_game(d, ai_menu)
            )
            btn.pack(pady=5, ipadx=10, ipady=5)
        
        ai_menu.grab_set()
    
    def start_ai_game(self, difficulty: str = "medium", menu_window: Optional[tk.Toplevel] = None):
        """Start a player vs AI game with specified difficulty."""
        if menu_window:
            menu_window.destroy()
        
        game_window = tk.Toplevel(self.root)
        game_window.title(f"Player vs AI ({difficulty.capitalize()})")
        game_window.geometry("550x700")
        TicTacToeGame(
            game_window, 
            mode="ai", 
            colors=self.colors, 
            fonts=self.fonts, 
            stats=self.stats,
            play_sound=self.play_sound,
            ai_difficulty=difficulty
        )


class TicTacToeGame:
    """Tic-Tac-Toe game implementation with enhanced features."""
    
    def __init__(
        self, 
        root: tk.Toplevel, 
        mode: str, 
        colors: Dict, 
        fonts: Dict, 
        stats: Dict,
        play_sound: callable,
        ai_difficulty: str = "medium"
    ):
        self.root = root
        self.mode = mode
        self.colors = colors
        self.fonts = fonts
        self.stats = stats
        self.play_sound = play_sound
        self.ai_difficulty = ai_difficulty
        
        self.root.configure(bg=self.colors['bg'])
        
        # Game state
        self.board = [""] * 9
        self.current_player = 0
        self.winning_line = None
        self.game_over = False
        self.move_start_time = None
        self.move_timer = None
        self.time_limit = 30  # seconds per move
        
        # Players configuration
        self.players = [
            {"name": "Player 1", "symbol": "X", "score": 0, "color": self.colors['x']},
            {"name": "AI" if mode == "ai" else "Player 2", "symbol": "O", "score": 0, "color": self.colors['o']}
        ]
        
        # Save/load functionality
        self.save_file = "tictactoe_save.json"
        
        # UI elements
        self.create_widgets()
        
        # Start move timer if it's a player's turn
        if not (self.mode == "ai" and self.current_player == 1):
            self.start_move_timer()
        
        # If AI's turn first
        if self.mode == "ai" and self.current_player == 1:
            self.root.after(500, self.ai_move)

    def create_widgets(self):
        """Create the game interface widgets."""
        # Header frame
        self.header_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=10, pady=10)
        self.header_frame.pack(fill=tk.X)
        
        # Score display
        self.score_label = tk.Label(
            self.header_frame,
            text=f"{self.players[0]['name']}: {self.players[0]['score']}  |  {self.players[1]['name']}: {self.players[1]['score']}",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.score_label.pack(side=tk.LEFT)
        
        # Timer display
        self.timer_label = tk.Label(
            self.header_frame,
            text=f"Time left: {self.time_limit}s",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['timer']
        )
        self.timer_label.pack(side=tk.RIGHT)
        
        # Turn indicator
        self.turn_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.turn_frame.pack(fill=tk.X, pady=5)
        
        self.turn_label = tk.Label(
            self.turn_frame,
            text=f"{self.players[self.current_player]['name']}'s turn ({self.players[self.current_player]['symbol']})",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.players[self.current_player]['color']
        )
        self.turn_label.pack()
        
        # Difficulty indicator for AI games
        if self.mode == "ai":
            self.difficulty_label = tk.Label(
                self.turn_frame,
                text=f"AI Difficulty: {self.ai_difficulty.capitalize()}",
                font=self.fonts['header'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            )
            self.difficulty_label.pack()
        
        # Game board
        self.board_frame = tk.Frame(self.root, bg=self.colors['grid'], padx=10, pady=10)
        self.board_frame.pack(pady=20)
        
        # Create board buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=self.fonts['board'],
                width=3,
                height=1,
                bg=self.colors['board_bg'],
                fg=self.colors['text'],
                activebackground=self.colors['secondary'],
                relief='flat',
                borderwidth=0,
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, ipadx=10, ipady=10)
            self.buttons.append(btn)
        
        # Control buttons
        self.control_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=10, pady=10)
        self.control_frame.pack(fill=tk.X)
        
        self.save_btn = tk.Button(
            self.control_frame,
            text="Save Game",
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg=self.colors['text'],
            command=self.save_game
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(
            self.control_frame,
            text="Load Game",
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg=self.colors['text'],
            command=self.load_game
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(
            self.control_frame,
            text="New Game",
            font=self.fonts['button'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=self.reset_game
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.menu_btn = tk.Button(
            self.control_frame,
            text="Main Menu",
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg=self.colors['text'],
            command=self.return_to_menu
        )
        self.menu_btn.pack(side=tk.RIGHT, padx=5)
    
    def start_move_timer(self):
        """Start the timer for the current move."""
        if self.move_timer:
            self.root.after_cancel(self.move_timer)
        
        self.move_start_time = time.time()
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display and check for timeouts."""
        if self.game_over:
            return
            
        elapsed = time.time() - self.move_start_time
        time_left = max(0, self.time_limit - int(elapsed))
        
        self.timer_label.config(text=f"Time left: {time_left}s")
        
        if time_left <= 0:
            self.handle_timeout()
        else:
            self.move_timer = self.root.after(1000, self.update_timer)
    
    def handle_timeout(self):
        """Handle a player timeout."""
        self.play_sound('click')
        messagebox.showwarning(
            "Time's Up!",
            f"{self.players[self.current_player]['name']} took too long!",
            parent=self.root
        )
        
        # Switch players and continue game
        self.switch_player()
        self.start_move_timer()
    
    def make_move(self, index: int):
        """Handle a player's move."""
        if self.game_over or self.board[index] != "":
            self.play_sound('click')
            return
            
        if self.mode == "ai" and self.current_player == 1:
            self.play_sound('click')
            return  # Prevent player from making AI's move
            
        self.play_sound('move')
        self.update_board(index)
        
        # If in AI mode and game isn't over, let AI make a move
        if self.mode == "ai" and not self.game_over and self.current_player == 1:
            self.root.after(500, self.ai_move)
    
    def update_board(self, index: int):
        """Update the game board with a move."""
        player = self.players[self.current_player]
        self.board[index] = player["symbol"]
        
        # Update button appearance
        self.buttons[index].config(
            text=player["symbol"],
            fg=player["color"],
            state=tk.DISABLED
        )
        
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
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]               # diagonals
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
        
        if self.move_timer:
            self.root.after_cancel(self.move_timer)
        
        # Highlight winning line
        self.highlight_winning_line()
        
        # Update score display
        self.score_label.config(
            text=f"{self.players[0]['name']}: {self.players[0]['score']}  |  {self.players[1]['name']}: {self.players[1]['score']}"
        )
        
        # Disable all buttons
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        # Play win sound
        self.play_sound('win')
        
        # Update statistics
        if hasattr(self, 'stats_callback'):
            self.stats_callback(self.mode, player['name'])
        
        # Show win message
        messagebox.showinfo(
            "Game Over",
            f"{player['name']} wins!",
            parent=self.root
        )
    
    def highlight_winning_line(self):
        """Highlight the winning line on the board."""
        if not self.winning_line:
            return
            
        # Get button positions
        buttons = [self.buttons[i] for i in self.winning_line]
        
        # Change background color of winning buttons
        for btn in buttons:
            btn.config(bg=self.colors['win'])
    
    def check_draw(self) -> bool:
        """Check if the game is a draw."""
        return all(cell != "" for cell in self.board) and not self.winning_line
    
    def handle_draw(self):
        """Handle a draw condition."""
        self.game_over = True
        self.turn_label.config(text="It's a draw!")
        
        if self.move_timer:
            self.root.after_cancel(self.move_timer)
        
        # Play draw sound
        self.play_sound('draw')
        
        # Update statistics
        if hasattr(self, 'stats_callback'):
            self.stats_callback(self.mode, None)
        
        messagebox.showinfo("Game Over", "The game is a draw!", parent=self.root)
    
    def switch_player(self):
        """Switch to the next player."""
        self.current_player = 1 - self.current_player
        player = self.players[self.current_player]
        
        self.turn_label.config(
            text=f"{player['name']}'s turn ({player['symbol']})",
            fg=player["color"]
        )
        
        # Start timer for the new player's move
        if not (self.mode == "ai" and self.current_player == 1):
            self.start_move_timer()
        else:
            if self.move_timer:
                self.root.after_cancel(self.move_timer)
    
    def ai_move(self):
        """Make a move for the AI player based on difficulty level."""
        if self.game_over:
            return
            
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if not empty_cells:
            return
            
        if self.ai_difficulty == "easy":
            # Random moves
            move = random.choice(empty_cells)
        elif self.ai_difficulty == "medium":
            # Sometimes blocks or wins, sometimes random
            if random.random() < 0.7:  # 70% chance to make a smart move
                move = self.find_smart_move()
            else:
                move = random.choice(empty_cells)
        elif self.ai_difficulty == "hard":
            # Always blocks or wins if possible, otherwise random
            move = self.find_smart_move()
        else:  # unbeatable
            # Uses minimax algorithm for perfect play
            move = self.find_best_move()
        
        self.play_sound('move')
        self.update_board(move)
    
    def find_smart_move(self) -> int:
        """Find a smart move (win if possible, block if needed, otherwise random)."""
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
            if self.check_win():
                self.board[i] = ""
                return i
            self.board[i] = ""
        
        # If center is available, take it
        if self.board[4] == "":
            return 4
        
        # Otherwise random
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_cells)
    
    def find_best_move(self) -> int:
        """Find the best move using minimax algorithm."""
        best_score = -float('inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.players[1]["symbol"]
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move if best_move is not None else random.choice(
            [i for i, cell in enumerate(self.board) if cell == ""]
        )
    
    def minimax(self, board: List[str], depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm for AI decision making."""
        # Evaluate the current board state
        result = self.evaluate_board(board)
        if result is not None:
            return result
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = self.players[1]["symbol"]
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = self.players[0]["symbol"]
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score
    
    def evaluate_board(self, board: List[str]) -> Optional[int]:
        """Evaluate the board state for minimax."""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        # Check for wins
        for pattern in win_patterns:
            if board[pattern[0]] != "" and all(board[i] == board[pattern[0]] for i in pattern):
                if board[pattern[0]] == self.players[1]["symbol"]:
                    return 10  # AI wins
                else:
                    return -10  # Player wins
        
        # Check for draw
        if all(cell != "" for cell in board):
            return 0  # Draw
        
        return None  # Game not over
    
    def save_game(self):
        """Save the current game state to a file."""
        game_state = {
            'mode': self.mode,
            'board': self.board,
            'current_player': self.current_player,
            'players': self.players,
            'game_over': self.game_over,
            'winning_line': self.winning_line,
            'ai_difficulty': self.ai_difficulty,
            'move_start_time': time.time() - self.move_start_time if self.move_start_time else 0
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(game_state, f)
            messagebox.showinfo("Game Saved", "Your game has been saved successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game: {str(e)}", parent=self.root)
    
    def load_game(self):
        """Load a game state from file."""
        if not os.path.exists(self.save_file):
            messagebox.showerror("Error", "No saved game found!", parent=self.root)
            return
        
        try:
            with open(self.save_file, 'r') as f:
                game_state = json.load(f)
            
            # Validate loaded game state
            if not all(key in game_state for key in ['mode', 'board', 'current_player', 'players']):
                raise ValueError("Invalid game save file")
            
            # Update game state
            self.mode = game_state['mode']
            self.board = game_state['board']
            self.current_player = game_state['current_player']
            self.players = game_state['players']
            self.game_over = game_state.get('game_over', False)
            self.winning_line = game_state.get('winning_line')
            self.ai_difficulty = game_state.get('ai_difficulty', 'medium')
            
            # Update UI
            self.reset_ui()
            
            # Restore timer if game isn't over
            if not self.game_over:
                elapsed_time = game_state.get('move_start_time', 0)
                self.move_start_time = time.time() - elapsed_time
                self.update_timer()
            
            messagebox.showinfo("Game Loaded", "Your game has been loaded successfully!", parent=self.root)
            
            # If it's AI's turn after loading
            if self.mode == "ai" and self.current_player == 1 and not self.game_over:
                self.root.after(500, self.ai_move)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {str(e)}", parent=self.root)
    
    def reset_ui(self):
        """Reset the UI based on current game state."""
        # Update board buttons
        for i in range(9):
            if self.board[i] == "":
                self.buttons[i].config(text="", state=tk.NORMAL, bg=self.colors['board_bg'])
            else:
                player = next(p for p in self.players if p['symbol'] == self.board[i])
                self.buttons[i].config(
                    text=player['symbol'],
                    fg=player['color'],
                    state=tk.DISABLED,
                    bg=self.colors['board_bg']
                )
        
        # Update turn display
        if not self.game_over:
            player = self.players[self.current_player]
            self.turn_label.config(
                text=f"{player['name']}'s turn ({player['symbol']})",
                fg=player["color"]
            )
        else:
            self.turn_label.config(text="Game Over")
        
        # Update score display
        self.score_label.config(
            text=f"{self.players[0]['name']}: {self.players[0]['score']}  |  {self.players[1]['name']}: {self.players[1]['score']}"
        )
        
        # Update difficulty display
        if hasattr(self, 'difficulty_label'):
            self.difficulty_label.config(text=f"AI Difficulty: {self.ai_difficulty.capitalize()}")
        
        # Highlight winning line if game is over
        if self.game_over and self.winning_line:
            self.highlight_winning_line()
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.board = [""] * 9
        self.winning_line = None
        self.game_over = False
        self.current_player = 0
        
        # Reset UI
        for btn in self.buttons:
            btn.config(
                text="",
                state=tk.NORMAL,
                bg=self.colors['board_bg'],
                fg=self.colors['text']
            )
        
        # Reset turn display
        player = self.players[self.current_player]
        self.turn_label.config(
            text=f"{player['name']}'s turn ({player['symbol']})",
            fg=player["color"]
        )
        
        # Reset timer
        self.start_move_timer()
        
        # If AI's turn first
        if self.mode == "ai" and self.current_player == 1:
            self.root.after(500, self.ai_move)
    
    def return_to_menu(self):
        """Return to the main menu."""
        if self.move_timer:
            self.root.after_cancel(self.move_timer)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()