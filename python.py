import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import time
import json
import os

class CyberSudokuPro:
    def __init__(self, root):
        self.root = root
        self.root.title("SUDOKU 🕸")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set adaptive window size (90% of screen, but max 1200x800)
        self.window_width = min(int(screen_width * 0.9), 1200)
        self.window_height = min(int(screen_height * 0.9), 800)
        
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.configure(bg='#0a0a12')
        
        # Prevent resizing (to avoid layout issues)
        self.root.resizable(False, False)
        
        # Calculate adaptive cell size based on window size
        self.cell_size = max(40, int(min(self.window_width, self.window_height) * 0.06))
        
        # Game settings
        self.board_size = 9
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.user_board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = []
        self.game_time = 0
        self.timer_running = False
        self.mistakes = 0
        self.score = 1000
        self.current_difficulty = "medium"
        self.selected_cell = None
        
        # Cyberpunk color scheme
        self.colors = {
            'bg': '#0a0a12',
            'bg_dark': '#05050a',
            'grid_bg': '#0f0f1a',
            'cell_bg': '#1a1a2e',
            'cell_alt': '#232339',
            'cell_fixed': '#16213e',
            'cell_selected': '#3a0ca3',
            'cell_highlight': '#4361ee',
            'text': '#ffffff',
            'text_secondary': '#b8b8d1',
            'text_glow': '#00f5ff',
            'primary': '#00f5ff',
            'primary_dark': '#0077b6',
            'success': '#00ff9d',
            'warning': '#ffd166',
            'error': '#ff0055',
            'accent': '#9d00ff',
            'accent2': '#7209b7',
            'grid_line': '#4a4a6a',
            'box_line': '#00f5ff',
            'glow_light': '#4cc9f0',
            'glow_medium': '#00f5ff',
            'glow_strong': '#00a8ff'
        }
        
        # Calculate adaptive font sizes based on window size
        self.title_font_size = max(24, int(self.window_width * 0.03))
        self.subtitle_font_size = max(14, int(self.window_width * 0.015))
        self.button_font_size = max(12, int(self.window_width * 0.012))
        self.cell_font_size = max(18, int(self.window_width * 0.018))
        self.timer_font_size = max(14, int(self.window_width * 0.012))
        self.stats_font_size = max(10, int(self.window_width * 0.01))
        
        # Fonts
        try:
            self.title_font = ('Courier', self.title_font_size, 'bold')
            self.subtitle_font = ('Courier', self.subtitle_font_size, 'bold')
            self.button_font = ('Courier', self.button_font_size, 'bold')
            self.cell_font = ('Courier', self.cell_font_size, 'bold')
            self.timer_font = ('Courier', self.timer_font_size, 'bold')
            self.stats_font = ('Courier', self.stats_font_size)
        except:
            self.title_font = ('Arial', self.title_font_size, 'bold')
            self.subtitle_font = ('Arial', self.subtitle_font_size, 'bold')
            self.button_font = ('Arial', self.button_font_size, 'bold')
            self.cell_font = ('Arial', self.cell_font_size, 'bold')
            self.timer_font = ('Arial', self.timer_font_size, 'bold')
            self.stats_font = ('Arial', self.stats_font_size)
        
        # Player data
        self.player_data = {
            'best_score': 0,
            'best_time': 99999,
            'games_played': 0,
            'total_wins': 0,
            'total_hints': 0
        }
        
        # Load player data
        self.load_player_data()
        
        # Center window on screen
        self.center_window()
        
        # Start with main menu
        self.show_main_menu()
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.show_main_menu())
        self.root.bind('<Control-n>', lambda e: self.start_game(self.current_difficulty))
        self.root.bind('<Control-h>', lambda e: self.give_hint())
        self.root.bind('<Control-s>', lambda e: self.solve_puzzle())
        
        # Bind number keys
        for i in range(1, 10):
            self.root.bind(str(i), lambda e, num=i: self.input_keyboard_number(num))
        self.root.bind('<Delete>', lambda e: self.input_keyboard_number(0))
        self.root.bind('<BackSpace>', lambda e: self.input_keyboard_number(0))
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_main_menu(self):
        """Show main menu"""
        if self.timer_running:
            self.timer_running = False
        
        self.clear_window()
        
        # Main container with padding
        padding_x = max(20, int(self.window_width * 0.02))
        padding_y = max(20, int(self.window_height * 0.02))
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=padding_x, pady=padding_y)
        
        # Title with adaptive spacing
        title_padding = max(20, int(self.window_height * 0.04))
        
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(pady=title_padding)
        
        # Main title
        tk.Label(
            title_frame,
            text="SUDOKU 🕸",
            font=self.title_font,
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack()
        
        tk.Label(
            title_frame,
            text="THE ULTIMATE 9×9 PUZZLE EXPERIENCE",
            font=self.subtitle_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        ).pack(pady=10)
        
        # Difficulty selection with adaptive spacing
        diff_padding = max(20, int(self.window_height * 0.03))
        diff_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        diff_frame.pack(pady=diff_padding)
        
        tk.Label(
            diff_frame,
            text="SELECT DIFFICULTY:",
            font=self.subtitle_font,
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 20))
        
        difficulties = [
            ("🚀 EASY", "45+ given numbers", "#00ff9d"),
            ("⚡ MEDIUM", "35-44 given numbers", "#00f5ff"),
            ("🔥 HARD", "30-34 given numbers", "#ffd166"),
            ("💀 EXPERT", "25-29 given numbers", "#ff0055"),
            ("👑 MASTER", "20-24 given numbers", "#9d00ff")
        ]
        
        # Calculate adaptive button sizes
        button_padx = max(40, int(self.window_width * 0.04))
        button_pady = max(10, int(self.window_height * 0.01))
        
        for diff, desc, color in difficulties:
            btn_frame = tk.Frame(diff_frame, bg=self.colors['bg'])
            btn_frame.pack(pady=8)
            
            btn = tk.Button(
                btn_frame,
                text=diff,
                font=self.button_font,
                bg=self.colors['bg_dark'],
                fg=color,
                activebackground=self.colors['grid_bg'],
                activeforeground=color,
                relief='flat',
                bd=4,
                highlightthickness=2,
                highlightbackground=color,
                highlightcolor=color,
                padx=button_padx,
                pady=button_pady,
                cursor='hand2',
                command=lambda d=diff.split()[1].lower(): self.start_game(d)
            )
            btn.pack()
            
            tk.Label(
                btn_frame,
                text=desc,
                font=self.stats_font,
                fg=self.colors['text_secondary'],
                bg=self.colors['bg']
            ).pack()
        
        # Player stats
        stats_padding = max(20, int(self.window_height * 0.03))
        stats_frame = tk.Frame(
            main_frame,
            bg=self.colors['cell_bg'],
            relief='ridge',
            bd=3,
            highlightbackground=self.colors['primary'],
            highlightthickness=2
        )
        stats_frame.pack(pady=stats_padding, ipadx=20, ipady=10)
        
        tk.Label(
            stats_frame,
            text="📊 PLAYER STATISTICS",
            font=self.button_font,
            fg=self.colors['primary'],
            bg=self.colors['cell_bg']
        ).pack(pady=10)
        
        stats_data = [
            ("🏆 Best Score:", str(self.player_data['best_score'])),
            ("⏱️ Best Time:", f"{self.player_data['best_time']}s" if self.player_data['best_time'] < 99999 else "N/A"),
            ("🎮 Games Played:", str(self.player_data['games_played'])),
            ("✅ Total Wins:", str(self.player_data['total_wins'])),
            ("💡 Hints Used:", str(self.player_data['total_hints']))
        ]
        
        for label, value in stats_data:
            row_frame = tk.Frame(stats_frame, bg=self.colors['cell_bg'])
            row_frame.pack(pady=3)
            
            tk.Label(
                row_frame,
                text=label,
                font=self.stats_font,
                fg=self.colors['text_secondary'],
                bg=self.colors['cell_bg']
            ).pack(side='left', padx=(0, 10))
            
            tk.Label(
                row_frame,
                text=value,
                font=self.stats_font,
                fg=self.colors['success'],
                bg=self.colors['cell_bg']
            ).pack(side='left')
        
        # Footer with adaptive padding
        footer_padding = max(10, int(self.window_height * 0.02))
        tk.Label(
            main_frame,
            text="ESC: Menu • CTRL+N: New Game • CTRL+H: Hint • CTRL+S: Solve • 1-9: Input Numbers",
            font=self.stats_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        ).pack(side='bottom', pady=footer_padding)
    
    def start_game(self, difficulty):
        """Start a new game"""
        self.current_difficulty = difficulty
        self.game_time = 0
        self.mistakes = 0
        self.score = 1000
        self.selected_cell = None
        
        # Generate fresh puzzle
        self.generate_fresh_puzzle()
        
        # Show game screen
        self.show_game_screen()
        
        # Start timer
        self.start_timer()
    
    def generate_fresh_puzzle(self):
        """Generate a completely new random puzzle"""
        # Create complete solved board
        self.generate_complete_board()
        
        # Copy to solution
        self.solution = [row[:] for row in self.board]
        self.original_board = [row[:] for row in self.board]
        
        # Remove numbers based on difficulty
        cells_to_keep = {
            'easy': random.randint(45, 50),
            'medium': random.randint(35, 44),
            'hard': random.randint(30, 34),
            'expert': random.randint(25, 29),
            'master': random.randint(20, 24)
        }[self.current_difficulty]
        
        cells_to_remove = 81 - cells_to_keep
        self.remove_cells(cells_to_remove)
        
        # Initialize user board
        self.user_board = [row[:] for row in self.board]
    
    def generate_complete_board(self):
        """Generate a complete valid Sudoku board"""
        # Start with empty board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal boxes first (they are independent)
        for box in range(0, 9, 3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            index = 0
            for i in range(3):
                for j in range(3):
                    self.board[box + i][box + j] = numbers[index]
                    index += 1
        
        # Fill remaining cells using backtracking
        self.solve_sudoku(self.board)
    
    def solve_sudoku(self, board):
        """Solve Sudoku using backtracking"""
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.is_valid_move(board, row, col, num):
                board[row][col] = num
                
                if self.solve_sudoku(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def find_empty(self, board):
        """Find empty cell"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid_move(self, board, row, col, num):
        """Check if move is valid"""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        
        return True
    
    def remove_cells(self, count):
        """Remove cells while maintaining unique solution"""
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        removed = 0
        attempts = 0
        
        while removed < count and attempts < 100 and cells:
            row, col = cells.pop()
            
            if self.board[row][col] != 0:
                # Store original value
                temp = self.board[row][col]
                self.board[row][col] = 0
                
                # Check if still has unique solution
                if self.has_unique_solution():
                    removed += 1
                else:
                    # Restore if not unique
                    self.board[row][col] = temp
                
                attempts += 1
    
    def has_unique_solution(self):
        """Check if puzzle has unique solution"""
        # Count solutions
        board_copy = [row[:] for row in self.board]
        return self.count_solutions(board_copy) == 1
    
    def count_solutions(self, board, count=0):
        """Count number of solutions"""
        if count > 1:
            return count
        
        empty = self.find_empty(board)
        if not empty:
            return count + 1
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid_move(board, row, col, num):
                board[row][col] = num
                count = self.count_solutions(board, count)
                board[row][col] = 0
                if count > 1:
                    break
        
        return count
    
    def show_game_screen(self):
        """Show game interface"""
        self.clear_window()
        
        # Calculate adaptive padding
        padding_x = max(10, int(self.window_width * 0.01))
        padding_y = max(10, int(self.window_height * 0.01))
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=padding_x, pady=padding_y)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, padding_y))
        
        # Back button
        tk.Button(
            header_frame,
            text="◀ MAIN MENU",
            font=self.button_font,
            bg=self.colors['cell_bg'],
            fg=self.colors['text'],
            command=self.show_main_menu,
            relief='flat',
            bd=2,
            padx=20,
            pady=5
        ).pack(side='left')
        
        # Stats display
        stats_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        stats_frame.pack(side='right')
        
        # Timer
        self.timer_label = tk.Label(
            stats_frame,
            text="⏱️ 00:00",
            font=self.timer_font,
            fg=self.colors['primary'],
            bg=self.colors['bg'],
            padx=10
        )
        self.timer_label.pack(side='left', padx=10)
        
        # Score
        self.score_label = tk.Label(
            stats_frame,
            text=f"🏆 {self.score}",
            font=self.timer_font,
            fg=self.colors['success'],
            bg=self.colors['bg'],
            padx=10
        )
        self.score_label.pack(side='left', padx=10)
        
        # Mistakes
        self.mistakes_label = tk.Label(
            stats_frame,
            text=f"⚡ {self.mistakes}/5",
            font=self.timer_font,
            fg=self.colors['warning'],
            bg=self.colors['bg'],
            padx=10
        )
        self.mistakes_label.pack(side='left', padx=10)
        
        # Difficulty badge
        diff_colors = {
            'easy': '#00ff9d',
            'medium': '#00f5ff',
            'hard': '#ffd166',
            'expert': '#ff0055',
            'master': '#9d00ff'
        }
        
        tk.Label(
            header_frame,
            text=self.current_difficulty.upper(),
            font=('Courier' if hasattr(self, 'button_font') and self.button_font[0] == 'Courier' else 'Arial', 
                  max(12, int(self.window_width * 0.012)), 'bold'),
            fg=diff_colors[self.current_difficulty],
            bg=self.colors['bg'],
            bd=3,
            relief='ridge',
            padx=15,
            pady=5
        ).pack(side='right', padx=20)
        
        # Game area
        game_area = tk.Frame(main_frame, bg=self.colors['bg'])
        game_area.pack(fill='both', expand=True)
        
        # Calculate board vs controls ratio
        board_width = int(self.window_width * 0.6)
        controls_width = int(self.window_width * 0.4)
        
        # Sudoku board container
        board_container = tk.Frame(game_area, bg=self.colors['grid_bg'])
        board_container.pack(side='left', padx=(0, 20))
        
        # Create board with thicker borders for 3x3 boxes
        self.cells = []
        for i in range(9):
            row_cells = []
            for j in range(9):
                # Alternate cell colors for visual distinction
                if (i // 3 + j // 3) % 2 == 0:
                    cell_bg = self.colors['cell_bg']
                else:
                    cell_bg = self.colors['cell_alt']
                
                # Cell frame
                cell_frame = tk.Frame(
                    board_container,
                    bg=self.colors['grid_line'],
                    width=self.cell_size,
                    height=self.cell_size
                )
                
                # Thicker borders for 3x3 boxes
                padx = (0, 4 if (j + 1) % 3 == 0 else 1)
                pady = (0, 4 if (i + 1) % 3 == 0 else 1)
                
                cell_frame.grid(row=i, column=j, padx=padx, pady=pady)
                cell_frame.pack_propagate(False)
                
                # Cell entry
                cell_var = tk.StringVar()
                entry = tk.Entry(
                    cell_frame,
                    textvariable=cell_var,
                    font=self.cell_font,
                    justify='center',
                    bg=cell_bg,
                    fg=self.colors['text'],
                    bd=0,
                    relief='flat',
                    width=2,
                    insertbackground=self.colors['primary']
                )
                entry.pack(fill='both', expand=True)
                
                # Set initial value
                if self.board[i][j] != 0:
                    cell_var.set(str(self.board[i][j]))
                    entry.config(
                        state='readonly',
                        fg=self.colors['success'],
                        readonlybackground=cell_bg
                    )
                else:
                    entry.config(fg=self.colors['text'])
                    # Bind events
                    entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.on_cell_change(r, c))
                    entry.bind('<FocusIn>', lambda e, r=i, c=j: self.select_cell(r, c))
                    entry.bind('<Button-1>', lambda e, r=i, c=j: self.select_cell(r, c))
                
                row_cells.append({
                    'entry': entry,
                    'var': cell_var,
                    'frame': cell_frame,
                    'bg': cell_bg
                })
            
            self.cells.append(row_cells)
        
        # Controls panel
        controls_frame = tk.Frame(
            game_area,
            bg=self.colors['cell_bg'],
            relief='ridge',
            bd=3,
            highlightbackground=self.colors['primary'],
            highlightthickness=2
        )
        controls_frame.pack(side='right', fill='both', expand=True)
        
        # Controls title
        tk.Label(
            controls_frame,
            text="🔧 CONTROL PANEL",
            font=self.button_font,
            fg=self.colors['primary'],
            bg=self.colors['cell_bg']
        ).pack(pady=20)
        
        # Control buttons
        controls = [
            ("💡 GET HINT (Ctrl+H)", self.give_hint),
            ("✓ CHECK SELECTED CELL", self.check_selected_cell),
            ("🔍 VALIDATE ALL CELLS", self.validate_all),
            ("🔄 NEW GAME (Ctrl+N)", lambda: self.start_game(self.current_difficulty)),
            ("🤖 AUTO SOLVE (Ctrl+S)", self.solve_puzzle),
            ("📊 SHOW STATISTICS", self.show_statistics)
        ]
        
        button_pady = max(5, int(self.window_height * 0.005))
        
        for text, command in controls:
            btn = tk.Button(
                controls_frame,
                text=text,
                font=self.stats_font,
                bg=self.colors['grid_bg'],
                fg=self.colors['text'],
                activebackground=self.colors['primary_dark'],
                activeforeground=self.colors['text'],
                relief='raised',
                bd=2,
                padx=10,
                pady=button_pady,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=button_pady, fill='x', padx=20)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['primary_dark']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['grid_bg']))
        
        # Number pad
        numpad_frame = tk.Frame(controls_frame, bg=self.colors['cell_bg'])
        numpad_frame.pack(pady=20)
        
        tk.Label(
            numpad_frame,
            text="🔢 QUICK INPUT",
            font=self.stats_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['cell_bg']
        ).pack(pady=(0, 10))
        
        # Number buttons
        numbers_grid = tk.Frame(numpad_frame, bg=self.colors['cell_bg'])
        numbers_grid.pack()
        
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for idx, num in enumerate(numbers):
            row = idx // 3
            col = idx % 3
            
            btn = tk.Button(
                numbers_grid,
                text=str(num),
                font=self.cell_font,
                bg=self.colors['grid_bg'],
                fg=self.colors['primary'],
                width=3,
                height=1,
                command=lambda n=num: self.input_number(n)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['primary_dark']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['grid_bg']))
        
        # Clear button
        clear_btn = tk.Button(
            numbers_grid,
            text="CLEAR",
            font=self.stats_font,
            bg=self.colors['error'],
            fg=self.colors['text'],
            width=9,
            height=1,
            command=lambda: self.input_number(0)
        )
        clear_btn.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky='nsew')
        
        # Instructions
        tk.Label(
            controls_frame,
            text="Click a cell to select • Use number keys or buttons to input",
            font=('Arial', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['cell_bg']
        ).pack(pady=20)
    
    def select_cell(self, row, col):
        """Select a cell and highlight related cells"""
        self.selected_cell = (row, col)
        
        # Reset all highlights
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:  # Only editable cells
                    self.cells[i][j]['entry'].config(bg=self.cells[i][j]['bg'])
        
        # Highlight selected cell
        self.cells[row][col]['entry'].config(bg=self.colors['cell_selected'])
        
        # Highlight same row and column
        for i in range(9):
            if i != col and self.board[row][i] == 0:
                self.cells[row][i]['entry'].config(bg=self.colors['cell_highlight'])
            if i != row and self.board[i][col] == 0:
                self.cells[i][col]['entry'].config(bg=self.colors['cell_highlight'])
        
        # Highlight same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(3):
            for j in range(3):
                r = box_row + i
                c = box_col + j
                if self.board[r][c] == 0 and not (r == row and c == col):
                    self.cells[r][c]['entry'].config(bg=self.colors['cell_highlight'])
    
    def input_keyboard_number(self, number):
        """Input number from keyboard"""
        if self.selected_cell:
            row, col = self.selected_cell
            self.input_number(number, row, col)
    
    def input_number(self, number, row=None, col=None):
        """Input number into selected cell"""
        if not self.selected_cell and (row is None or col is None):
            messagebox.showinfo("Select Cell", "Please select a cell first!")
            return
        
        if row is None or col is None:
            row, col = self.selected_cell
        
        # Check if cell is editable
        if self.board[row][col] != 0:
            messagebox.showinfo("Fixed Cell", "This cell contains a fixed number!")
            return
        
        if number == 0:
            # Clear the cell
            self.cells[row][col]['var'].set("")
            self.user_board[row][col] = 0
            self.cells[row][col]['entry'].config(fg=self.colors['text'])
        else:
            # Set the number
            self.cells[row][col]['var'].set(str(number))
            self.on_cell_change(row, col)
    
    def on_cell_change(self, row, col):
        """Handle cell value change"""
        value = self.cells[row][col]['var'].get().strip()
        
        if value == '':
            self.user_board[row][col] = 0
            self.cells[row][col]['entry'].config(fg=self.colors['text'])
            return
        
        # Allow only single digit
        if len(value) > 1:
            self.cells[row][col]['var'].set(value[0])
            value = value[0]
        
        if value.isdigit():
            num = int(value)
            
            if 1 <= num <= 9:
                # Check if correct
                if num == self.solution[row][col]:
                    self.user_board[row][col] = num
                    self.cells[row][col]['entry'].config(fg=self.colors['success'])
                    
                    # Award points
                    self.score += 10
                    self.score_label.config(text=f"🏆 {self.score}")
                    
                    # Check if puzzle complete
                    if self.is_puzzle_complete():
                        self.game_complete()
                else:
                    # Wrong number
                    self.cells[row][col]['entry'].config(fg=self.colors['error'])
                    self.mistakes += 1
                    self.mistakes_label.config(text=f"⚡ {self.mistakes}/5")
                    
                    # Penalty
                    self.score = max(0, self.score - 20)
                    self.score_label.config(text=f"🏆 {self.score}")
                    
                    # Check for game over
                    if self.mistakes >= 5:
                        self.game_over()
            else:
                # Clear if 0
                self.cells[row][col]['var'].set("")
                self.user_board[row][col] = 0
        else:
            # Non-digit input
            self.cells[row][col]['var'].set("")
            self.user_board[row][col] = 0
    
    def give_hint(self):
        """Give a hint to player"""
        # Find empty cells
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.user_board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            messagebox.showinfo("Hint", "All cells are filled!")
            return
        
        # Pick random empty cell
        row, col = random.choice(empty_cells)
        
        # Show correct number
        correct = self.solution[row][col]
        self.cells[row][col]['var'].set(str(correct))
        self.user_board[row][col] = correct
        self.cells[row][col]['entry'].config(fg=self.colors['warning'])
        
        # Penalty for hint
        self.score = max(0, self.score - 50)
        self.score_label.config(text=f"🏆 {self.score}")
        self.player_data['total_hints'] += 1
        
        # Highlight the cell
        self.select_cell(row, col)
        
        messagebox.showinfo("Hint", f"Cell ({row+1}, {col+1}) = {correct}")
    
    def check_selected_cell(self):
        """Check the currently selected cell"""
        if not self.selected_cell:
            messagebox.showinfo("Check Cell", "Please select a cell first!")
            return
        
        row, col = self.selected_cell
        
        if self.board[row][col] != 0:
            messagebox.showinfo("Check Cell", "This is a fixed number!")
        elif self.user_board[row][col] == 0:
            messagebox.showinfo("Check Cell", "This cell is empty!")
        elif self.user_board[row][col] == self.solution[row][col]:
            messagebox.showinfo("Check Cell", "Correct! ✅")
        else:
            messagebox.showinfo("Check Cell", f"Wrong! Should be {self.solution[row][col]} ❌")
    
    def validate_all(self):
        """Check all filled cells"""
        incorrect = []
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.user_board[i][j] != 0:
                    if self.user_board[i][j] != self.solution[i][j]:
                        incorrect.append((i, j))
                        self.cells[i][j]['entry'].config(fg=self.colors['error'])
        
        if incorrect:
            messagebox.showwarning("Validation", f"Found {len(incorrect)} incorrect cells!")
        else:
            if self.is_puzzle_complete():
                self.game_complete()
            else:
                messagebox.showinfo("Validation", "All filled cells are correct! ✅")
    
    def solve_puzzle(self):
        """Auto-solve the puzzle"""
        if not messagebox.askyesno("Solve Puzzle", "This will solve the entire puzzle. Continue?"):
            return
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    correct = self.solution[i][j]
                    self.cells[i][j]['var'].set(str(correct))
                    self.user_board[i][j] = correct
                    self.cells[i][j]['entry'].config(fg=self.colors['accent'])
        
        self.timer_running = False
        messagebox.showinfo("Puzzle Solved", "The puzzle has been solved!")
    
    def show_statistics(self):
        """Show game statistics"""
        time_str = f"{self.game_time // 60:02d}:{self.game_time % 60:02d}"
        completion = self.calculate_completion()
        
        stats = f"""
        ⚡ GAME STATISTICS ⚡
        
        ⏱️  Time: {time_str}
        🏆  Score: {self.score}
        ⚡  Mistakes: {self.mistakes}/5
        🎯  Difficulty: {self.current_difficulty.upper()}
        📊  Completion: {completion}%
        🔢  Empty Cells: {self.count_empty_cells()}
        """
        
        messagebox.showinfo("Statistics", stats)
    
    def calculate_completion(self):
        """Calculate completion percentage"""
        total = 0
        filled = 0
        
        for i in range(9):
            for j in range(9):
                total += 1
                if self.user_board[i][j] != 0:
                    filled += 1
        
        return int((filled / total) * 100) if total > 0 else 0
    
    def count_empty_cells(self):
        """Count empty cells"""
        count = 0
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    count += 1
        return count
    
    def is_puzzle_complete(self):
        """Check if puzzle is complete"""
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def start_timer(self):
        """Start the game timer"""
        self.game_time = 0
        self.timer_running = True
        
        def update_timer():
            if self.timer_running:
                self.game_time += 1
                minutes = self.game_time // 60
                seconds = self.game_time % 60
                self.timer_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}")
                self.root.after(1000, update_timer)
        
        update_timer()
    
    def game_complete(self):
        """Handle game completion"""
        self.timer_running = False
        
        # Calculate final score
        time_penalty = max(0, (self.game_time - 300) // 30) * 5
        self.score = max(0, self.score - time_penalty - (self.mistakes * 30))
        
        # Update player data
        self.player_data['games_played'] += 1
        self.player_data['total_wins'] += 1
        
        if self.score > self.player_data['best_score']:
            self.player_data['best_score'] = self.score
        
        if self.game_time < self.player_data['best_time']:
            self.player_data['best_time'] = self.game_time
        
        self.save_player_data()
        
        # Show victory message
        time_str = f"{self.game_time // 60:02d}:{self.game_time % 60:02d}"
        message = f"""
        🎉 PUZZLE SOLVED! 🎉
        
        Time: {time_str}
        Score: {self.score}
        Mistakes: {self.mistakes}
        Difficulty: {self.current_difficulty.upper()}
        
        Congratulations!
        """
        
        messagebox.showinfo("Victory!", message)
        self.show_main_menu()
    
    def game_over(self):
        """Handle game over"""
        self.timer_running = False
        messagebox.showinfo("Game Over", "Too many mistakes! Try again.")
        self.show_main_menu()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def load_player_data(self):
        """Load player data from file"""
        try:
            if os.path.exists("sudoku_player_data.json"):
                with open("sudoku_player_data.json", "r") as f:
                    loaded = json.load(f)
                    self.player_data.update(loaded)
        except:
            pass
    
    def save_player_data(self):
        """Save player data to file"""
        try:
            with open("sudoku_player_data.json", "w") as f:
                json.dump(self.player_data, f, indent=4)
        except:
            pass


def main():
    """Main function"""
    root = tk.Tk()
    
    # Create game instance
    game = CyberSudokuPro(root)
    
    # Run main loop
    root.mainloop()


if __name__ == "__main__":
    main()
