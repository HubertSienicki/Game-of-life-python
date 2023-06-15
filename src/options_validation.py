import tkinter.simpledialog as sd
import tkinter.messagebox as mb


def validate_neighbors(value):
    try:
        value = int(value)
        if value < 1 or value > 8:
            mb.showerror(
                "Invalid input",
                "Neighbors for multiplication should be between 1 and 8",
            )
            return None
        return value
    except ValueError:
        mb.showerror(
            "Invalid input", "Neighbors for multiplication should be an integer"
        )
        return None


def validate_size(value):
    try:
        if "x" in value:
            rows, cols = map(int, value.split("x"))
            if rows < 5 or cols < 5:
                mb.showerror(
                    "Invalid input", "Both rows and columns should be at least 5"
                )
                return None
            return rows, cols
        else:
            mb.showerror(
                "Invalid input",
                "Size should be in the format 'axb' where a and b are integers",
            )
            return None
    except ValueError:
        mb.showerror(
            "Invalid input",
            "Size should be in the format 'axb' where a and b are integers",
        )
        return None


def show_options(parent, config):
    neighbors = sd.askinteger(
        "Options", "Enter the number of neighbors for multiplication", parent=parent
    )
    neighbors = validate_neighbors(neighbors)
    if neighbors is not None:
        config["neighbors"] = neighbors
    else:
        show_options(parent, config)

    size = sd.askstring(
        "Options", "Enter the size of the window (format 'axb')", parent=parent
    )
    size = validate_size(size)
    if size is not None:
        rows, cols = size
        config["rows"] = rows
        config["cols"] = cols
    else:
        show_options(parent, config)
