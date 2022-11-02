import tkinter as tk
import tkinter.font as font

# flake8: noqa


window = tk.Tk()
window.resizable(False, False)
window.title("Tic-Tac-Toe")

myFont = font.Font(family="Courier", size=20, weight="bold")
gridFont = font.Font(family="Courier", size=36, weight="bold")

label = tk.Label(window, text="Player X Turn", font=myFont, bg='LightSteelBlue4', fg='white')
label.grid(row=0, column=0)

play_area = tk.Frame(window, width=300, height=30, bg="honeydew2")
play_area.grid(row=1, column=0)


class State:
    current_char = "X"
    X_points = []
    O_points = []
    game_over = False
    buttons = {}
    square = None
    winning_positon = None


def update_label(text):
    label.configure(text=text)

def start_O():
    reset_button()
    State.current_char = "O"
    update_label("Player O Turn")

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.button = tk.Button(play_area, text=" ", width=5, height=2, command=self.btn_op, bg='gainsboro', font=gridFont, pady=10)

    def btn_op(self):
        if State.game_over is not True:
            if not self.value:
                self.value = State.current_char
                self.button.configure(text=State.current_char, bg="ivory4", fg="black")
                if State.current_char == "X":
                    State.current_char = "O"
                    State.X_points.append(self)
                    update_label("Player O Turn")
                else:
                    State.current_char = "X"
                    State.O_points.append(self)
                    update_label("Player X Turn")
                    
            check_win()

    def reset(self):
        self.button.configure(text="", bg="gainsboro")
        self.value = None

class WinningStates:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def check(self, for_char):
        p1_satisfied = False
        p2_satisfied = False
        p3_satisfied = False
        if for_char == "X":
            for coord in State.X_points:
                if coord.x == self.x1 and coord.y == self.y1:
                    p1_satisfied = True
                elif coord.x == self.x2 and coord.y == self.y2:
                    p2_satisfied = True
                elif coord.x == self.x3 and coord.y == self.y3:
                    p3_satisfied = True
        elif for_char == "O":
            for coord in State.O_points:
                if coord.x == self.x1 and coord.y == self.y1:
                    p1_satisfied = True
                elif coord.x == self.x2 and coord.y == self.y2:
                    p2_satisfied = True
                elif coord.x == self.x3 and coord.y == self.y3:
                    p3_satisfied = True
        return all([p1_satisfied, p2_satisfied, p3_satisfied])


for x in range(1, 4):
    for y in range(1, 4):
        State.buttons[(x, y)] = State.square = Square(x, y)
        State.square.button.grid(row=x, column=y, sticky='nsew')


winning_states = [
    WinningStates(1, 1, 1, 2, 1, 3),
    WinningStates(2, 1, 2, 2, 2, 3),
    WinningStates(3, 1, 3, 2, 3, 3),
    WinningStates(1, 1, 2, 1, 3, 1),
    WinningStates(1, 2, 2, 2, 3, 2),
    WinningStates(1, 3, 2, 3, 3, 3),
    WinningStates(1, 1, 2, 2, 3, 3),
    WinningStates(3, 1, 2, 2, 1, 3),
]


def show_winning_line(state):
    for x, y in [(state.x1, state.y1), (state.x2, state.y2), (state.x3, state.y3)]:
        square = State.buttons[(x, y)]
        square.button.configure(bg='yellow')

def check_win():
    for state in winning_states:
        if state.check("X"):
            update_label("Player X Wins")
            State.game_over = True
            show_winning_line(state)
            return
        if state.check("O"):
            update_label("Player O Wins")
            State.game_over = True
            show_winning_line(state)
            return
    if len(State.X_points) + len(State.O_points) == 9:
        update_label("Draw")


def reset_button():
    for State.square in State.buttons.values():
        State.square.reset()
    State.current_char = "X"
    State.X_points = []
    State.O_points = []
    State.game_over = False
    State.winning_positon = None
    update_label(f'Player {State.current_char} Turn')


reset_btn = tk.Button(window, text='Reset', font=myFont, command=reset_button)
reset_btn.grid(row=2, column=0)

menubar = tk.Menu(window)
game_menu = tk.Menu(menubar, tearoff= 0)
game_menu.add_command(label='Reset Game', command=reset_button)
game_menu.add_command(label='Start with O', command=start_O)
game_menu.add_separator()
game_menu.add_command(label='Exit', command= window.destroy)
menubar.add_cascade(label='Game', menu=game_menu)

window.config(menu=menubar)

window.mainloop()
