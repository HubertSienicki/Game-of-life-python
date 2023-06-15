import tkinter as tk
import tkinter.simpledialog as sd
import copy

config = {"neighbors": 3, "rows": 20, "cols": 20, "size": 20}

game_window = None  # Global variable to track the game window


class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.size = config["size"]
        self.board = self.create_board()
        self.rectangles = [[None] * self.cols for _ in range(self.rows)]
        self.is_paused = False

        self.options_button = tk.Button(
            master,
            text="Options",
            command=self.show_options,
            font=("Arial", 10),
            bg="blue",
            fg="white",
            width=15,
        )
        self.options_button.pack()

        self.canvas = tk.Canvas(
            master, width=self.cols * self.size, height=self.rows * self.size
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

        self.instruction_label = tk.Label(
            master, text="Press space to pause/start", font=("Arial", 10)
        )
        self.instruction_label.pack()

        master.bind("<space>", self.toggle_pause)

    def create_board(self):
        return [[0] * self.cols for _ in range(self.rows)]

    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 1:
                    fill = "black"
                else:
                    fill = "white"

                x1 = j * self.size
                y1 = i * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size

                self.rectangles[i][j] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill
                )

    def handle_click(self, event):
        col = event.x // self.size
        row = event.y // self.size
        self.board[row][col] = 1
        self.canvas.itemconfig(self.rectangles[row][col], fill="black")

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def show_options(self):
        self.is_paused = True
        show_options(self.master)
        if game_window:
            game_window.restart_game()

    def update(self):
        if not self.is_paused:
            new_board = copy.deepcopy(self.board)

            for i in range(self.rows):
                for j in range(self.cols):
                    total = self.count_neighbors(i, j)
                    if self.board[i][j] == 1:
                        if total < 2 or total > 3:
                            new_board[i][j] = 0
                    elif total == config["neighbors"]:
                        new_board[i][j] = 1

            self.board = new_board
            for i in range(self.rows):
                for j in range(self.cols):
                    color = "black" if self.board[i][j] == 1 else "white"
                    self.canvas.itemconfig(self.rectangles[i][j], fill=color)

        self.canvas.after(1000, self.update)

    def count_neighbors(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                count += self.board[i][j]
        count -= self.board[row][col]
        return count

    def restart_game(self):
        self.master.destroy()
        start_game()


def start_game():
    global game_window  # Use the global variable
    root = tk.Tk()
    game_window = GameOfLife(root)
    root.after(1000, game_window.update)
    set_window_center(
        root, game_window.cols * game_window.size, game_window.rows * game_window.size + 90
    )  # Increase window height to account for Options button and instruction label
    root.mainloop()


def show_options(parent):
    x = parent.winfo_x()
    y = parent.winfo_y()
    neighbors = sd.askinteger(
        "Options", "Enter the number of neighbors for multiplication", parent=parent
    )
    if neighbors is not None:
        config["neighbors"] = neighbors
    size = sd.askstring(
        "Options", "Enter the size of the window (format 'axb')", parent=parent
    )
    if size and "x" in size:
        rows, cols = map(int, size.split("x"))
        config["rows"] = rows
        config["cols"] = cols


def start_menu():
    menu = tk.Tk()
    menu.title("Game of Life")
    frame = tk.Frame(menu)
    frame.pack(expand=True)
    start_button = tk.Button(
        frame,
        text="Start",
        command=lambda: [start_game(), menu.destroy()],
        width=20,
        height=2,
        font=("Arial", 25),
        bg="blue",
        fg="white",
    )
    start_button.grid(row=0, column=0, pady=15)
    options_button = tk.Button(
        frame,
        text="Options",
        command=lambda: [show_options(menu)],
        width=20,
        height=2,
        font=("Arial", 25),
        bg="green",
        fg="white",
    )
    options_button.grid(row=1, column=0, pady=15)
    quit_button = tk.Button(
        frame,
        text="Quit",
        command=menu.quit,
        width=20,
        height=2,
        font=("Arial", 25),
        bg="red",
        fg="white",
    )
    quit_button.grid(row=2, column=0, pady=15)
    set_window_center(menu, 400, 480)  # Increase start menu size to fit larger buttons
    menu.mainloop()


def set_window_center(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))


start_menu()
