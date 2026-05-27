import tkinter as tk
import random

ROWS = 20
COLS = 20
CELL_SIZE = 25

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

root = tk.Tk()
root.title("Game of Life - Empty Starter Grid")

is_running = False
DELAY = 120

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

count_label = tk.Label(root, text="Alive Cells: 0", font=("Arial", 12, "bold"))
count_label.pack(pady=5)


def make_empty_board():
    new_board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(0)
        new_board.append(row)
    return new_board

board = make_empty_board()


def count_neighbors(r, c):
    alive_neighbors = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            neighbor_row = (r + dr) % ROWS
            neighbor_col = (c + dc) % COLS

            if board[neighbor_row][neighbor_col] == 1:
                alive_neighbors += 1
    return alive_neighbors


def step():
    global board

    new_board = make_empty_board()

    for r in range(ROWS):
        for c in range(COLS):
            n = count_neighbors(r, c)

            if board[r][c] == 1:
                if n == 2 or n == 3:
                    new_board[r][c] = 1
                else:
                    new_board[r][c] = 0
            else:
                if n == 3:
                    new_board[r][c] = 1
                else:
                    new_board[r][c] = 0

    board = new_board
    draw_board()

    if is_running:
        root.after(DELAY, step)


def run_simulation():
    global is_running
    if not is_running:
        is_running = True
        run_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)
        step()


def stop_simulation():
    global is_running
    is_running = False
    run_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)


def change_speed(val):
    global DELAY
    DELAY = int(val)


def draw_cell(r, c):
    x1 = c * CELL_SIZE
    y1 = r * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    color = "Medium Sea Green" if board[r][c] == 1 else "white"
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def update_alive_count():
    alive_count = sum(sum(row) for row in board)
    count_label.config(text=f"Alive Cells: {alive_count}")

def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(r, c)
    update_alive_count()

def toggle_cell(event):
    c = event.x // CELL_SIZE
    r = event.y // CELL_SIZE
    if 0 <= r < ROWS and 0 <= c < COLS:
        board[r][c] = 1 - board[r][c]
        draw_board()

canvas.bind("<Button-1>", toggle_cell)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

def clear_board():
    stop_simulation()
    global board
    board = make_empty_board()
    draw_board()

def random_board():
    for r in range(ROWS):
        for c in range(COLS):
            board[r][c] = random.randint(0, 1)
    draw_board()

clear_btn = tk.Button(button_frame, text="Clear", command=clear_board)
clear_btn.grid(row=0, column=0, padx=5)

rand_btn = tk.Button(button_frame, text="Random", command=random_board)
rand_btn.grid(row=0, column=1, padx=5)

next_btn = tk.Button(button_frame, text="Next Gen", command=lambda: step() if not is_running else None)
next_btn.grid(row=0, column=2, padx=5)

run_btn = tk.Button(button_frame, text="Run", command=run_simulation, bg="#A9DFBF", font=("Arial", 10, "bold"))
run_btn.grid(row=0, column=3, padx=5)

stop_btn = tk.Button(button_frame, text="Stop", command=stop_simulation, bg="#F1948A", font=("Arial", 10, "bold"),
                     state=tk.DISABLED)
stop_btn.grid(row=0, column=4, padx=5)

speed_frame = tk.Frame(root)
speed_frame.pack(pady=5)

speed_label = tk.Label(speed_frame, text="Delay (ms):", font=("Arial", 10))
speed_label.grid(row=0, column=0, padx=2)

speed_slider = tk.Scale(speed_frame, from_=20, to=600, orient=tk.HORIZONTAL, command=change_speed)
speed_slider.set(DELAY)
speed_slider.grid(row=0, column=1, padx=5)

draw_board()
root.mainloop()