import tkinter as tk
import random

BOARD_SIZE = 15
CELL_SIZE = 36  # pixels per cell
STONE_RADIUS = 14
MARGIN = 30
RAINBOW_COLORS = [
    'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'
]
PLAYER_NAMES = ['Player 1', 'Player 2']
COLOR_MAP = {
    'red': '#FF0000',
    'orange': '#FFA500',
    'yellow': '#FFFF00',
    'green': '#008000',
    'blue': '#0000FF',
    'indigo': '#4B0082',
    'violet': '#8F00FF',
    'black': '#000000',
    'white': '#FFFFFF',
}

class Stone:
    def __init__(self, color, owner):
        self.color = color
        self.owner = owner

class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Gomoku')
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.exit_fullscreen)
        self.exit_button.pack(anchor='ne', padx=8, pady=8)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        self.show_mode_selection()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_mode_selection(self):
        self.clear_main_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        title = tk.Label(self.main_frame, text="Choose Game Mode", font=("Arial", 24))
        title.grid(row=0, column=0, columnspan=2, pady=(40, 20))
        # Rainbow button
        rainbow_btn = tk.Frame(self.main_frame, bd=3, relief='raised', cursor='hand2', bg='white')
        rainbow_btn.grid(row=1, column=0, sticky='nsew', padx=40, pady=40)
        rainbow_btn.grid_propagate(False)
        rainbow_btn.update_idletasks()
        # Center rainbow icon and text
        rainbow_inner = tk.Frame(rainbow_btn, bg='white')
        rainbow_inner.place(relx=0.5, rely=0.5, anchor='center')
        rainbow_canvas = tk.Canvas(rainbow_inner, width=7*32, height=32, highlightthickness=0, bg='white')
        for i, color in enumerate(RAINBOW_COLORS):
            x = 16 + i*32
            rainbow_canvas.create_oval(x-13, 16-13, x+13, 16+13, fill=COLOR_MAP[color], outline='black')
        rainbow_canvas.pack()
        rainbow_label = tk.Label(rainbow_inner, text="Rainbow\nHidden-Ownership", font=("Arial", 20), bg='white')
        rainbow_label.pack(pady=(10,0))
        for widget in [rainbow_btn, rainbow_inner, rainbow_canvas, rainbow_label]:
            widget.bind('<Button-1>', lambda e: self.select_mode('rainbow', '🌈'))
        # Regular button
        regular_btn = tk.Frame(self.main_frame, bd=3, relief='raised', cursor='hand2', bg='white')
        regular_btn.grid(row=1, column=1, sticky='nsew', padx=40, pady=40)
        regular_btn.grid_propagate(False)
        regular_inner = tk.Frame(regular_btn, bg='white')
        regular_inner.place(relx=0.5, rely=0.5, anchor='center')
        regular_icon = tk.Label(regular_inner, text="⚫⚪", font=("Arial", 40), bg='white')
        regular_icon.pack()
        regular_label = tk.Label(regular_inner, text="Regular\nGomoku", font=("Arial", 20), bg='white')
        regular_label.pack(pady=(10,0))
        for widget in [regular_btn, regular_inner, regular_icon, regular_label]:
            widget.bind('<Button-1>', lambda e: self.select_mode('regular', '⚫⚪'))

    def select_mode(self, mode, icon):
        self.game_type = mode
        self.game_type_icon = icon
        self.show_player_selection()

    def show_player_selection(self):
        self.clear_main_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        title = tk.Label(self.main_frame, text="Choose Player Mode", font=("Arial", 24))
        title.grid(row=0, column=0, columnspan=2, pady=(40, 20))
        btn1 = tk.Button(self.main_frame, text="👥\nTwo Players", font=("Arial", 20), width=16, height=5, command=lambda: self.select_player_mode(False, '👥'))
        btn1.grid(row=1, column=0, sticky='nsew', padx=40, pady=40)
        btn2 = tk.Button(self.main_frame, text="🤖\nPlay vs AI", font=("Arial", 20), width=16, height=5, command=lambda: self.select_player_mode(True, '🤖'))
        btn2.grid(row=1, column=1, sticky='nsew', padx=40, pady=40)

    def select_player_mode(self, ai_mode, icon):
        self.ai_mode = ai_mode
        self.player_mode_icon = icon
        if ai_mode:
            self.show_ai_difficulty_selection()
        else:
            self.show_rules_window()

    def show_ai_difficulty_selection(self):
        self.clear_main_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        title = tk.Label(self.main_frame, text="Choose AI Difficulty", font=("Arial", 24))
        title.grid(row=0, column=0, columnspan=3, pady=(40, 20))
        btn0 = tk.Button(self.main_frame, text="Random\n(just valid moves)", font=("Arial", 20), width=16, height=5, command=lambda: self.select_ai_difficulty('random'))
        btn0.grid(row=1, column=0, sticky='nsew', padx=40, pady=40)
        btn1 = tk.Button(self.main_frame, text="Easy\n(random/block/win)", font=("Arial", 20), width=16, height=5, command=lambda: self.select_ai_difficulty('easy'))
        btn1.grid(row=1, column=1, sticky='nsew', padx=40, pady=40)
        btn2 = tk.Button(self.main_frame, text="Harder\n(lookahead 2 moves)", font=("Arial", 20), width=16, height=5, command=lambda: self.select_ai_difficulty('harder'))
        btn2.grid(row=1, column=2, sticky='nsew', padx=40, pady=40)

    def select_ai_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        self.show_rules_window()

    def show_rules_window(self):
        self.clear_main_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        rules = (
            "Rainbow Hidden-Ownership Gomoku Rules:\n"
            "- Players alternate turns placing stones on the intersections.\n"
            "- Each stone is secretly owned by the player who placed it.\n"
            "- When placing, the player chooses any rainbow color for the stone.\n"
            "- The board only shows the color, not the owner.\n"
            "- Stones must be placed adjacent to any existing stone (except the first move).\n"
            "- When someone gets five in a row (by ownership), they win.\n"
            "- At the end, ownership is revealed (1 = Player 1, 2 = Player 2/AI)."
        ) if self.game_type == 'rainbow' else (
            "Regular Gomoku Rules:\n"
            "- Players alternate turns placing black and white stones on the intersections.\n"
            "- Stones must be placed adjacent to any existing stone (except the first move).\n"
            "- The first to get five in a row (horizontally, vertically, or diagonally) wins."
        )
        rules_label = tk.Label(self.main_frame, text=rules, font=("Arial", 18), justify='left', padx=32, pady=32)
        rules_label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        start_btn = tk.Button(self.main_frame, text="Start Game", font=("Arial", 18, 'bold'), command=self.start_game)
        start_btn.grid(row=1, column=0, columnspan=2, pady=(0,32))

    def start_game(self):
        self.clear_main_frame()
        container = tk.Frame(self.main_frame)
        container.place(relx=0.5, rely=0.5, anchor='center')
        self.top_label = tk.Label(container, text=f"Mode: {self.game_type_icon}   Players: {self.player_mode_icon}", font=("Arial", 18))
        self.top_label.pack(pady=(0, 10))
        self.canvas = tk.Canvas(container, width=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), height=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), bg='#F5DEB3')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        controls = tk.Frame(container)
        controls.pack(fill='x', pady=(10,0))
        self.status_label = tk.Label(controls, text=f"{PLAYER_NAMES[0]}'s turn", font=("Arial", 14))
        self.status_label.pack(side='left', padx=10)
        self.confirm_button = tk.Button(controls, text="Confirm Move", font=("Arial", 14), command=self.confirm_move, state='disabled')
        self.confirm_button.pack(side='right', padx=10)
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 0
        self.total_moves = 0
        self.selected = None
        self.ownership_revealed = False
        self.draw_board()
        if self.ai_mode and self.current_player == 1:
            self.disable_board()
            self.root.after(500, self.ai_move)
        else:
            self.enable_board()

    def ask_gomoku_type_buttons(self):
        win = tk.Toplevel(self.root)
        win.title("Choose Gomoku Mode")
        win.grab_set()
        tk.Label(win, text="Choose Game Mode", font=("Arial", 16)).pack(pady=10)
        result = {}
        def pick(mode, icon):
            result['mode'] = mode
            result['icon'] = icon
            win.destroy()
        # Rainbow button with color circles
        rainbow_frame = tk.Frame(win, bd=2, relief='raised', cursor='hand2')
        rainbow_canvas = tk.Canvas(rainbow_frame, width=7*22, height=22, highlightthickness=0, bg=win.cget('bg'))
        for i, color in enumerate(RAINBOW_COLORS):
            x = 11 + i*22
            rainbow_canvas.create_oval(x-9, 11-9, x+9, 11+9, fill=COLOR_MAP[color], outline='black')
        rainbow_canvas.pack()
        rainbow_label = tk.Label(rainbow_frame, text="Rainbow Hidden-Ownership", font=("Arial", 14))
        rainbow_label.pack(pady=(0,4))
        rainbow_frame.pack(pady=8, padx=8, fill='x')
        rainbow_frame.bind('<Button-1>', lambda e: pick('rainbow', '🌈'))
        rainbow_canvas.bind('<Button-1>', lambda e: pick('rainbow', '🌈'))
        rainbow_label.bind('<Button-1>', lambda e: pick('rainbow', '🌈'))
        # Regular button
        btn2 = tk.Button(win, text="⚫⚪\nRegular Gomoku", font=("Arial", 16), width=16, height=3, command=lambda: pick('regular', '⚫⚪'))
        btn2.pack(pady=8)
        win.wait_window()
        return result['mode'], result['icon']

    def ask_game_mode_buttons(self):
        win = tk.Toplevel(self.root)
        win.title("Choose Player Mode")
        win.grab_set()
        tk.Label(win, text="Choose Player Mode", font=("Arial", 16)).pack(pady=10)
        result = {}
        def pick(ai, icon):
            result['ai'] = ai
            result['icon'] = icon
            win.destroy()
        btn1 = tk.Button(win, text="👥\nTwo Players", font=("Arial", 16), width=16, height=3, command=lambda: pick(False, '👥'))
        btn1.pack(pady=8)
        btn2 = tk.Button(win, text="🤖\nPlay vs AI", font=("Arial", 16), width=16, height=3, command=lambda: pick(True, '🤖'))
        btn2.pack(pady=8)
        win.wait_window()
        return result['ai'], result['icon']

    def draw_board(self):
        self.canvas.delete('all')
        # Draw grid lines
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, x, MARGIN + CELL_SIZE * (BOARD_SIZE-1), x)
            self.canvas.create_line(x, MARGIN, x, MARGIN + CELL_SIZE * (BOARD_SIZE-1))
        # Draw star points (hoshi)
        for i in [3, 7, 11]:
            for j in [3, 7, 11]:
                self.canvas.create_oval(
                    MARGIN + i*CELL_SIZE - 3, MARGIN + j*CELL_SIZE - 3,
                    MARGIN + i*CELL_SIZE + 3, MARGIN + j*CELL_SIZE + 3,
                    fill='black')
        # Draw stones
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                stone = self.board[r][c]
                if stone is not None:
                    self.draw_stone(r, c, stone.color, stone.owner)
        # Draw selection highlight
        if self.selected:
            r, c = self.selected
            x, y = self.coord_to_pixel(r, c)
            self.canvas.create_oval(x-STONE_RADIUS-2, y-STONE_RADIUS-2, x+STONE_RADIUS+2, y+STONE_RADIUS+2, outline='red', width=2)

    def coord_to_pixel(self, row, col):
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        return x, y

    def pixel_to_coord(self, x, y):
        # Find nearest intersection
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            px, py = self.coord_to_pixel(row, col)
            # Only allow if click is close enough to intersection
            if abs(px - x) <= CELL_SIZE//2 and abs(py - y) <= CELL_SIZE//2:
                return row, col
        return None, None

    def is_valid_move(self, row, col):
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False
        if self.board[row][col] is not None:
            return False
        if self.total_moves == 0:
            return True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if self.board[nr][nc] is not None:
                        return True
        return False

    def get_all_valid_moves(self):
        valid = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.is_valid_move(r, c):
                    valid.append((r, c))
        return valid

    def on_canvas_click(self, event):
        if not hasattr(self, 'board_enabled') or not self.board_enabled:
            return
        row, col = self.pixel_to_coord(event.x, event.y)
        if row is None or not self.is_valid_move(row, col):
            return
        # Unselect previous
        self.selected = (row, col)
        self.confirm_button.config(state='normal')
        self.draw_board()

    def confirm_move(self):
        if not self.selected:
            return
        row, col = self.selected
        if self.game_type == 'rainbow':
            self.show_color_buttons(row, col)
        else:
            color = 'black' if self.current_player == 0 else 'white'
            self.place_stone(row, col, color, self.current_player)
            self.selected = None
            self.confirm_button.config(state='disabled')
            self.draw_board()
            if self.check_five_in_a_row(self.current_player):
                self.end_game(f"{PLAYER_NAMES[self.current_player]} wins with five in a row!")
                return
            self.current_player = 1 - self.current_player
            self.total_moves += 1
            self.status_label.config(text=f"{PLAYER_NAMES[self.current_player]}'s turn")
            if self.ai_mode and self.current_player == 1:
                self.disable_board()
                self.root.after(500, self.ai_move)
            elif self.total_moves >= BOARD_SIZE * BOARD_SIZE:
                self.end_game("No five in a row for either player. It's a draw!")
            else:
                self.enable_board()

    def show_color_buttons(self, row, col):
        self.disable_board()
        self.color_button_frame = tk.Frame(self.root)
        self.color_button_frame.pack(pady=10)
        for color in RAINBOW_COLORS:
            btn = tk.Button(self.color_button_frame, bg=COLOR_MAP[color], width=4, height=2, command=lambda c=color: self.pick_color(row, col, c))
            btn.pack(side='left', padx=4)

    def pick_color(self, row, col, color):
        self.color_button_frame.destroy()
        self.place_stone(row, col, color, self.current_player)
        self.selected = None
        self.confirm_button.config(state='disabled')
        self.draw_board()
        if self.check_five_in_a_row(self.current_player):
            self.reveal_ownership()
            self.draw_board()
            self.end_game(f"{PLAYER_NAMES[self.current_player]} wins with five in a row!")
            return
        self.current_player = 1 - self.current_player
        self.total_moves += 1
        self.status_label.config(text=f"{PLAYER_NAMES[self.current_player]}'s turn")
        if self.ai_mode and self.current_player == 1:
            self.disable_board()
            self.root.after(500, self.ai_move)
        elif self.total_moves >= BOARD_SIZE * BOARD_SIZE:
            self.reveal_ownership()
            self.draw_board()
            self.end_game("No five in a row for either player. It's a draw!")
        else:
            self.enable_board()

    def enable_board(self):
        self.board_enabled = True
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def disable_board(self):
        self.board_enabled = False
        self.canvas.unbind('<Button-1>')

    # In ai_move, use self.ai_difficulty to select the AI logic
    def ai_move(self):
        difficulty = getattr(self, 'ai_difficulty', 'easy')
        if difficulty == 'harder':
            row, col, color = self.harder_ai_move()
        elif difficulty == 'easy':
            row, col, color = self.easy_ai_move()
        else:  # random
            row, col, color = self.random_ai_move()
        self.place_stone(row, col, color, 1)
        self.draw_board()
        if self.check_five_in_a_row(1):
            if self.game_type == 'rainbow':
                self.reveal_ownership()
                self.draw_board()
            self.end_game(f"{PLAYER_NAMES[1]} wins with five in a row!")
            return
        self.current_player = 0
        self.total_moves += 1
        self.status_label.config(text=f"{PLAYER_NAMES[self.current_player]}'s turn")
        self.enable_board()

    def easy_ai_move(self):
        valid_moves = self.get_all_valid_moves()
        ai_owner = 1
        human_owner = 0
        # 1. Try to win
        for row, col in valid_moves:
            for color in (RAINBOW_COLORS if self.game_type == 'rainbow' else ['white']):
                self.board[row][col] = Stone(color, ai_owner)
                if self.check_five_in_a_row(ai_owner):
                    self.board[row][col] = None
                    chosen_color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else color
                    return row, col, chosen_color
                self.board[row][col] = None
        # 2. Block human win
        for row, col in valid_moves:
            for color in (RAINBOW_COLORS if self.game_type == 'rainbow' else ['black']):
                self.board[row][col] = Stone(color, human_owner)
                if self.check_five_in_a_row(human_owner):
                    self.board[row][col] = None
                    block_color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else 'white'
                    return row, col, block_color
                self.board[row][col] = None
        # 3. Otherwise, random
        row, col = random.choice(valid_moves)
        color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else 'white'
        return row, col, color

    def harder_ai_move(self):
        valid_moves = self.get_all_valid_moves()
        ai_owner = 1
        human_owner = 0
        # 1. Try to win now
        for row, col in valid_moves:
            for color in (RAINBOW_COLORS if self.game_type == 'rainbow' else ['white']):
                self.board[row][col] = Stone(color, ai_owner)
                if self.check_five_in_a_row(ai_owner):
                    self.board[row][col] = None
                    chosen_color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else color
                    return row, col, chosen_color
                self.board[row][col] = None
        # 2. Block human win now
        for row, col in valid_moves:
            for color in (RAINBOW_COLORS if self.game_type == 'rainbow' else ['black']):
                self.board[row][col] = Stone(color, human_owner)
                if self.check_five_in_a_row(human_owner):
                    self.board[row][col] = None
                    block_color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else 'white'
                    return row, col, block_color
                self.board[row][col] = None
        # 3. Score all moves for AI (favor longest line, double threats)
        best_moves = []
        best_score = -1
        for row, col in valid_moves:
            for color in (RAINBOW_COLORS if self.game_type == 'rainbow' else ['white']):
                self.board[row][col] = Stone(color, ai_owner)
                score = self.evaluate_move(row, col, ai_owner)
                double_threat = self.count_open_fours(row, col, ai_owner) >= 2
                if double_threat:
                    score += 1000
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col, color)]
                elif score == best_score:
                    best_moves.append((row, col, color))
                self.board[row][col] = None
        if best_moves:
            row, col, _ = random.choice(best_moves)
            color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else 'white'
            return row, col, color
        # 4. Otherwise, random
        row, col = random.choice(valid_moves)
        color = self.choose_confusing_color(row, col) if self.game_type == 'rainbow' else 'white'
        return row, col, color

    def evaluate_move(self, row, col, owner):
        # Return the length of the longest line (open or closed) for this move
        max_len = 1
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr, dc in directions:
            count = 1
            # Forward
            r, c = row+dr, col+dc
            while 0<=r<BOARD_SIZE and 0<=c<BOARD_SIZE and self.board[r][c] is not None and self.board[r][c].owner == owner:
                count += 1
                r += dr
                c += dc
            # Backward
            r, c = row-dr, col-dc
            while 0<=r<BOARD_SIZE and 0<=c<BOARD_SIZE and self.board[r][c] is not None and self.board[r][c].owner == owner:
                count += 1
                r -= dr
                c -= dc
            if count > max_len:
                max_len = count
        return max_len

    def count_open_fours(self, row, col, owner):
        # Count the number of open-ended lines of 4 for this move
        count = 0
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr, dc in directions:
            line = [(row, col)]
            # Forward
            r, c = row+dr, col+dc
            while 0<=r<BOARD_SIZE and 0<=c<BOARD_SIZE and self.board[r][c] is not None and self.board[r][c].owner == owner:
                line.append((r,c))
                r += dr
                c += dc
            # Backward
            r, c = row-dr, col-dc
            while 0<=r<BOARD_SIZE and 0<=c<BOARD_SIZE and self.board[r][c] is not None and self.board[r][c].owner == owner:
                line.append((r,c))
                r -= dr
                c -= dc
            if len(line) == 4:
                # Check both ends are open
                ends = []
                fr, fc = line[0][0]-dr, line[0][1]-dc
                br, bc = line[-1][0]+dr, line[-1][1]+dc
                for rr, cc in [(fr, fc), (br, bc)]:
                    if 0<=rr<BOARD_SIZE and 0<=cc<BOARD_SIZE and self.board[rr][cc] is None:
                        ends.append(True)
                    else:
                        ends.append(False)
                if all(ends):
                    count += 1
        return count

    def random_ai_move(self):
        valid_moves = self.get_all_valid_moves()
        row, col = random.choice(valid_moves)
        color = random.choice(RAINBOW_COLORS) if self.game_type == 'rainbow' else 'white'
        return row, col, color

    def place_stone(self, row, col, color, owner):
        self.board[row][col] = Stone(color, owner)
        # Drawing is handled in draw_board

    def draw_stone(self, row, col, color, owner):
        x, y = self.coord_to_pixel(row, col)
        self.canvas.create_oval(x-STONE_RADIUS, y-STONE_RADIUS, x+STONE_RADIUS, y+STONE_RADIUS, fill=COLOR_MAP[color], outline='black')
        # For rainbow mode, show number on reveal only
        if self.game_type == 'rainbow' and hasattr(self, 'ownership_revealed') and self.ownership_revealed:
            self.canvas.create_text(x, y, text=str(owner+1), fill='white' if color in ['red', 'blue', 'indigo', 'violet', 'green', 'black'] else 'black', font=('Arial', 16, 'bold'))

    def check_five_in_a_row(self, owner):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] is None or self.board[r][c].owner != owner:
                    continue
                # Horizontal
                if c <= BOARD_SIZE - 5 and all(
                    self.board[r][c + i] is not None and self.board[r][c + i].owner == owner for i in range(5)
                ):
                    return True
                # Vertical
                if r <= BOARD_SIZE - 5 and all(
                    self.board[r + i][c] is not None and self.board[r + i][c].owner == owner for i in range(5)
                ):
                    return True
                # Diagonal \
                if r <= BOARD_SIZE - 5 and c <= BOARD_SIZE - 5 and all(
                    self.board[r + i][c + i] is not None and self.board[r + i][c + i].owner == owner for i in range(5)
                ):
                    return True
                # Diagonal /
                if r >= 4 and c <= BOARD_SIZE - 5 and all(
                    self.board[r - i][c + i] is not None and self.board[r - i][c + i].owner == owner for i in range(5)
                ):
                    return True
        return False

    def reveal_ownership(self):
        self.ownership_revealed = True

    def end_game(self, message):
        # If AI wins, change message
        if self.ai_mode and ("Player 2 wins" in message or message.startswith("Player 2")):
            message = message.replace("Player 2", "AI")
        self.clear_main_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        end_frame = tk.Frame(self.main_frame)
        end_frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(end_frame, text=message, font=("Arial", 24), pady=20).pack()
        btn_frame = tk.Frame(end_frame)
        btn_frame.pack(pady=20)
        play_again = tk.Button(btn_frame, text="Play Again", font=("Arial", 18), width=12, command=self.show_mode_selection)
        play_again.pack(side='left', padx=20)
        if self.ai_mode:
            if self.ai_difficulty == 'harder':
                try_same = tk.Button(btn_frame, text="Try Same AI", font=("Arial", 18), width=14, command=lambda: self.select_ai_difficulty('harder'))
                try_same.pack(side='left', padx=20)
            else:
                next_diff = 'easy' if self.ai_difficulty == 'random' else 'harder'
                try_harder = tk.Button(btn_frame, text="Try Harder AI", font=("Arial", 18), width=14, command=lambda: self.select_ai_difficulty(next_diff))
                try_harder.pack(side='left', padx=20)
        exit_btn = tk.Button(btn_frame, text="Exit", font=("Arial", 18), width=12, command=self.exit_fullscreen)
        exit_btn.pack(side='right', padx=20)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        self.root.quit()

    def choose_confusing_color(self, row, col):
        # Prefer the most recently used human color
        last_human_color = None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                stone = self.board[r][c]
                if stone is not None and stone.owner == 0:
                    last_human_color = stone.color
        # Prefer a color present in the neighborhood
        neighbor_colors = set()
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    stone = self.board[nr][nc]
                    if stone is not None:
                        neighbor_colors.add(stone.color)
        # Try to use the last human color if possible
        if last_human_color and last_human_color in RAINBOW_COLORS:
            return last_human_color
        # Try to use a neighbor color
        if neighbor_colors:
            return random.choice(list(neighbor_colors))
        # Otherwise, random
        return random.choice(RAINBOW_COLORS)

if __name__ == '__main__':
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop() 
