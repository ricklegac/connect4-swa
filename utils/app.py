"""
Ricardo Leguizamon
Diego Seo
Lorenzo Cabrea

"""
import random, time
import tkinter as tk
from .utils import ordinal
"""
La clase Board es la que se encarga de simular la tabla
En este caso tenemos las siguientes propiedades
    b.rows          # numero de filas en el juego
    b.cols          # numero de columnas en el juego
    b.PLAYER1       # una bandera que representa al jugador 1 
    b.PLAYER2       # una bandera que representa al jugador 2 
    b.EMPTY_SLOT    # bandera que representa un espacio vacio 
"""
class Board(object):

    EMPTY_SLOT = 0 # al comienzo todos tienen que estar vacios no 6x7 
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, rows, cols):
        self._board = [
            [self.EMPTY_SLOT]*cols for _ in range(rows)
        ]
        self.rows = rows
        self.cols = cols
    
    def __getitem__(self, key):
        return self._board[key[0]][key[1]]
    
    def get(self, row, col=None):
        return self.__getitem__(row if col is None else (row, col))
    
    def occupied(self, row, col=None):
        return self.__getitem__(row if col is None else (row, col)) != self.EMPTY_SLOT
    
    def placeable(self, col):
        return self._board[0][col] == self.EMPTY_SLOT

    def place(self, player, col):
        assert(player == self.PLAYER1 or player == self.PLAYER2)
        for r in reversed(self._board):
            if r[col] == self.EMPTY_SLOT:
                r[col] = player
                return True
        raise ValueError("Column {} is not placeable.".format(col))

    def has_draw(self):
        for r in self._board:
            for c in r:
                if c == self.EMPTY_SLOT:
                    return False
        return True
    
    def who_wins(self):
        rows = list(map(lambda r: "".join(map(str, r)), self._board))
        cols = list(map(lambda c: "".join(map(str, c)), zip(*self._board)))
        left_revolved = [
            [self.EMPTY_SLOT]*r+self._board[r]+[self.EMPTY_SLOT]*(self.rows-1-r) for r in range(self.rows)
        ]
        left_diag = list(map(lambda d: "".join(map(str, d)), zip(*left_revolved)))
        right_revolved = [
            [self.EMPTY_SLOT]*(self.rows-1-r)+self._board[r]+[self.EMPTY_SLOT]*r for r in range(self.rows)
        ]
        right_diag = list(map(lambda d: "".join(map(str, d)), zip(*right_revolved)))
        seg = rows + cols + left_diag + right_diag
        p1 = "".join(map(str, [self.PLAYER1]*4))
        for s in seg:
            if p1 in s:
                return self.PLAYER1
        p2 = "".join(map(str, [self.PLAYER2]*4))
        for s in seg:
            if p2 in s:
                return self.PLAYER2
        return None

    def terminal(self):
        return self.has_draw() or self.who_wins() is not None
    
    def clone(self):
        b = Board(self.rows, self.cols)
        b._board = [[c for c in r] for r in self._board]
        return b
    
    def row(self, r):
        return [e for e in self._board[r]]
    
    def col(self, c):
        return [self._board[r][c] for r in range(self.rows)]

    def dump(self, indent=0):
        return "\n".join([" "*indent + "{}".format(r) for r in self._board])
    
    def __str__(self):
        return self.dump()


class App(tk.Frame):
    
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6

    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self, alg_fn_map, master=None):
        super().__init__(master)
        self.alg_fn_map = alg_fn_map

        self.master.title("Busqueda con Adversario - Conecta4")

        self.master.geometry("640x480")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black")
        self.canvas.grid(row=0, column=0, columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=28
        )
        self.bt_new = tk.Button(self.master, text="Nuevo Juego", command=self.new_game)
        self.bt_new.grid(row=1, column=0,
            sticky=tk.W, padx=10, pady=(0, 10)
        )

        self.master.columnconfigure(0, weight=0)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=0)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)

        self.new_game_window = None

    def new_game(self):
        if self.new_game_window is not None:
            # self.new_game_window.destroy()
            # self.new_game_window = None
            self.new_game_window.update()
            self.new_game_window.deiconify()
            return

        self.new_game_window = tk.Toplevel(self.master)
        self.new_game_window.title("Nuevo Juego")
        # self.new_game_window.attributes("-topmost", True)
        # self.new_game_window.grab_set()
        self.new_game_window.protocol("WM_DELETE_WINDOW", self.new_game_window.withdraw)
        self.new_game_window.resizable(False, False)
    
        player1_var = tk.StringVar(self.new_game_window)
        player2_var = tk.StringVar(self.new_game_window)
        listbox_player1 = tk.OptionMenu(self.new_game_window, player1_var, "IA")
        listbox_player2 = tk.OptionMenu(self.new_game_window, player2_var, "IA", "Humano")
        player1_depth_var = tk.StringVar(self.new_game_window)
        player2_depth_var = tk.StringVar(self.new_game_window)
        listbox_player1_depth = tk.OptionMenu(self.new_game_window, player1_depth_var, "1", "2", "3", "4", "5")
        listbox_player2_depth = tk.OptionMenu(self.new_game_window, player2_depth_var, "1", "2", "3", "4", "5")
        player1_depth_var.set("1")
        player2_depth_var.set("1")
        player1_var.set("IA")
        player2_var.set("IA")
        listbox_player1.config(width=6)
        listbox_player2.config(width=6)
        #listbox_player1_depth.config(state=tk.DISABLED)
        #listbox_player2_depth.config(state=tk.DISABLED)
        player1_var.trace("w",
            lambda *args: listbox_player1_depth.config(state=tk.NORMAL if player1_var.get() == "IA" else tk.DISABLED)
        )
        player2_var.trace("w",
            lambda *args: listbox_player2_depth.config(state=tk.NORMAL if player2_var.get() == "IA" else tk.DISABLED)
        )

        alg_var = tk.StringVar(self.new_game_window)
        alg_var.set(next(iter(self.alg_fn_map.keys())))
        listbox_alg = tk.OptionMenu(self.new_game_window, alg_var, *self.alg_fn_map.keys())

        def new_game():
            self.terminal_request = True
            # self.new_game_window.destroy()
            # self.new_game_window = None
            self.new_game_window.withdraw()
            self.run_game(
                player1_var.get(), int(player1_depth_var.get()),
                player2_var.get(), int(player2_depth_var.get()),
                self.alg_fn_map[alg_var.get()]
            )

        listbox_player1.grid(row=0, column=0, padx=10)
        listbox_player1_depth.grid(row=0, column=1, padx=10)
        tk.Label(self.new_game_window, text="v.s.").grid(row=0, column=2, padx=10)
        listbox_player2.grid(row=0, column=3, padx=10)
        listbox_player2_depth.grid(row=0, column=4, padx=10)

        listbox_alg.grid(row=1, columnspan=5, pady=5)

        tk.Button(
            self.new_game_window, text="Done", command=new_game
        ).grid(row=2, columnspan=5, pady=(20, 0))

        win_x = self.master.winfo_x()
        win_y = self.master.winfo_y()
        win_w = self.master.winfo_width()
        win_h = self.master.winfo_height()
        self.new_game_window.update()
        w = self.new_game_window.winfo_width()
        h = self.new_game_window.winfo_height()
        self.new_game_window.geometry("{}x{}+{}+{}".format(w, h, int(win_x+(win_w-w)*0.5), int(win_y+(win_h-h)*0.5)))


    def draw_checker(self, player, x, y, tag=""):
        c = "#c40003" if player == self.PLAYER1 else "white"
        self.canvas.create_oval(x, y,
            x+self.cell_size*0.9, y+self.cell_size*0.9,
            fill=c, outline="black", width=1,
            tag=tag
        )

    def prompt(self, msg):
        self.canvas.delete("msg")
        self.canvas.create_text(self.canvas.winfo_width()*0.5, 32,
            text=msg, fill="black", font=(None, 12), anchor="center"
        )

    def clear_canvas(self):
        self.canvas.delete("all")

    def run_game(self, player1, search_depth1, player2, search_depth2, search_fn):
        self.clear_canvas()
        self.terminal_request = False

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.cell_size = 20
        self.draw_checker(self.PLAYER1, 20, 20)
        self.canvas.create_text(20, 40,
            text=player1, fill="black", font=(None, 10), anchor="nw"
        )
        if player1 == "IA":
            self.canvas.create_text(20, 55,
                text="Profundidad: {}".format(search_depth1), fill="black", font=(None, 10), anchor="nw"
            )
        self.draw_checker(self.PLAYER2, w-40, 20)
        self.canvas.create_text(w-20, 40,
            text=player2, fill="black", font=(None, 10), anchor="ne"
        )
        if player2 == "IA":
            self.canvas.create_text(w-20, 55,
                text="Profundidad: {}".format(search_depth2), fill="black", font=(None, 10), anchor="ne"
            )
        h -= 10
        self.cell_size = min(
            w / self.BOARD_WIDTH,
            (h-60) / self.BOARD_HEIGHT
        )
        board_pos = (
            (w - self.cell_size*self.BOARD_WIDTH)*0.5,
            h - self.cell_size*self.BOARD_HEIGHT
        )
        for r in range(self.BOARD_HEIGHT+1):
            self.canvas.create_line(
                board_pos[0], board_pos[1] + r*self.cell_size,
                board_pos[0] + self.BOARD_WIDTH*self.cell_size, board_pos[1] + r*self.cell_size,
            )
        for c in range(self.BOARD_WIDTH+1):
            self.canvas.create_line(
                board_pos[0] + c*self.cell_size, board_pos[1],
                board_pos[0] + c*self.cell_size, board_pos[1] + self.BOARD_HEIGHT*self.cell_size,
            )
        
        self.board = Board(self.BOARD_HEIGHT, self.BOARD_WIDTH)

        def place(player, col, render=True):
            if self.board.place(player, col):
                print("Jugador {} en la columna {}".format(1 if player == self.PLAYER1 else 2, ordinal(col+1)))
                print(self.board.dump())
                print("############################################")
                if render:
                    row = next(r for r in range(self.board.rows) if self.board.occupied(r, col))
                    self.draw_checker(player, 
                        board_pos[0]+(col+0.05)*self.cell_size,
                        board_pos[1]+(row+0.05)*self.cell_size
                    )
                    self.canvas.update()
                return self.PLAYER2 if player == self.PLAYER1 else self.PLAYER1
            if player == "Humano":
                return player
            raise ValueError("IA intenta colocar en una columna invalida ({})".format(col))

        def human_motion(player, x, y, tag="last_human_motion"):
            x -= board_pos[0]
            col = int(x/self.cell_size)
            y -= board_pos[1]
            row = int(y/self.cell_size)
            self.canvas.delete("last_human_motion")
            if col > -1 and col < self.board.cols and \
               row > -1 and row < self.board.rows and \
               self.board.placeable(col):
                row = next(r for r in range(self.board.rows-1,-1,-1) if not self.board.occupied(r, col))
                self.draw_checker(player, 
                    board_pos[0]+(col+0.05)*self.cell_size,
                    board_pos[1]+(row+0.05)*self.cell_size,
                    tag=tag
                )
                return col
            return None
            
        def human_click(player, x, y):
            loc = human_motion(player, x, y, "")
            if loc is not None:
                adversary = place(player, loc, render=False)
                self.canvas.unbind("<Motion>")
                self.canvas.unbind("<1>")
                return turn_for(adversary)

        def turn_for(player):
            if self.terminal_request:
                return
            if self.board.has_draw():
                self.prompt("Empate")
                print("Juego termina en empate.")
                return
            winner = self.board.who_wins()
            if winner is not None:   
                self.prompt("Jugador {} gana".format(1 if winner == self.PLAYER1 else 2))
                print("Jugador {} gana.".format(1 if winner == self.PLAYER1 else 2))
                return
            agent = player1 if player == self.PLAYER1 else player2
            if agent == "Humano":
                self.canvas.bind("<Motion>", lambda e: human_motion(player, e.x, e.y))
                self.canvas.bind("<1>", lambda e: human_click(player, e.x, e.y))
                x = self.canvas.winfo_pointerx()-self.canvas.winfo_rootx()
                y = self.canvas.winfo_pointery()-self.canvas.winfo_rooty()
                human_motion(player, x, y)
            else:
                print("############################################")
                if agent == "Random":
                    m = []
                    for c in range(self.board.cols):
                        if self.board.placeable(c):
                            m.append(c)
                    action = random.choice(m)
                    time.sleep(0.1)
                else:
                    action, *_ = search_fn(player, self.board, search_depth1 if player == self.PLAYER1 else search_depth2)
                if action is None:
                    self.prompt("Jugador {} nu juega".format(1 if player == self.PLAYER1 else 2))
                    print("Jugador {} no juega".format(1 if player == self.PLAYER1 else 2))
                else:
                    adversary = place(player, action)
                    # self.master.bind("<Key>", lambda e: turn_for(adversary))
                    return turn_for(adversary)

        turn_for(self.PLAYER1)
