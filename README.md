🎮 Tic-Tac-Toe Ultimate

A modern, feature-rich, and beautifully designed Tic-Tac-Toe game built with Python, Tkinter, and AI (Minimax).

🚀 Features
✔ Multiple Game Modes

Player vs Player (PVP)

Player vs AI with 4 difficulty levels:

Easy (random)

Medium (semi-smart)

Hard (strategic)

Unbeatable (Minimax algorithm)

🧠 Artificial Intelligence

The AI uses different logic depending on chosen difficulty:

Easy → random moves

Medium → 70% chance to block/win

Hard → always blocks or wins if possible

Unbeatable → Minimax algorithm (perfect play, impossible to beat)

🕹️ Gameplay Features

Beautiful animated GUI using Tkinter

Player turn indicator

30-second timer per move

Auto timeout handling

Win/draw detection

Highlighting of the winning line

Live score tracking

📊 Game Statistics

Automatically saves lifetime stats to tictactoe_stats.json:

PVP wins

PVP draws

AI wins

AI draws

Total games played

💾 Save & Load System

You can save and load any match using:

Save Game button

Load Game button

Saves include:

Full board state

Player turn

AI difficulty

Timer state

Scores

Winning line

Stored in tictactoe_save.json.

🎨 Interface

Modern blue UI

Red "X", green "O"

Yellow highlight for winning moves

Responsive layout with headers, timers, menus
