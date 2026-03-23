import random
import time
import tkinter as tk

from game.alphabeta import AlphaBetaAlgo
from game.minimax import MinMaxAlgo
from gui.main_gui import GameGUI
from game.tree import SpecificState, SpecificTreeNode, makeTree


# Spēles loģikas un kontroles klase
class GameLogic:
    def __init__(self):
        # Izveido logu un piesaista GUI
        self.root = tk.Tk()
        self.gui = GameGUI(self.root)

        # Piesaista GUI pogas šī faila funkcijām
        self.gui.on_start_game = self.StartTheGame
        self.gui.on_number_clicked = self.MakeMoveGUI

        # Spēles mainīgie
        self.human_points = 100
        self.computer_points = 100
        self.array_of_numbers = []
        self.active_player = None
        self.settings = {}
        self.game_over = False

    # Sagatavo un sāk jaunu spēli
    def StartTheGame(self, settings):
        self.settings = settings
        self.human_points = 100
        self.computer_points = 100
        self.game_over = False
        self.active_player = settings["sacejs"]

        # Ģenerē skaitļu masīvu
        lenght_of_array = settings["garums"]
        self.array_of_numbers = [random.randint(1, 4) for _ in range(lenght_of_array)]

        self.gui.build_game_board(
            self.array_of_numbers, self.active_player, settings["algoritms"], lenght_of_array
        )

        # Ja datori sāk pirmais, iedarbina tā gājienu
        if self.active_player == "Dators":
            self.startPCTurn()

    # Apstrādā klikšķi (spēlētāja vai datora)
    def MakeMoveGUI(self, index):
        if self.game_over or self.array_of_numbers[index] is None:
            return

        number = self.array_of_numbers[index]

        # Punktu aprēķins
        if number % 2 == 0:
            points = number * 2
            if self.active_player == "Cilveks":
                self.human_points -= points
            else:
                self.computer_points -= points
        else:
            if self.active_player == "Cilveks":
                self.computer_points += number
            else:
                self.human_points += number

        # Atjauno GUI stāvokli
        self.array_of_numbers[index] = None
        self.gui.update_scores(self.human_points, self.computer_points)
        self.gui.remove_button(index)

        # Pārbauda, vai spēle beigusies
        if all(x is None for x in self.array_of_numbers):
            self.game_over = True
            self.chooseWinner()
            return

        # Maina aktīvo spēlētāju
        self.active_player = (
            "Dators" if self.active_player == "Cilveks" else "Cilveks"
        )
        self.gui.update_turn_indicator(self.active_player)

        # Izsauc datora gājienu, ja nepieciešams
        if self.active_player == "Dators":
            self.startPCTurn()

    # Nobloķē pogas un ieplāno datora gājienu
    def startPCTurn(self):
        self.gui.set_buttons_state("disabled")
        self.root.after(800, self.makeMovePC)

    # Datora loģika (Minimax vai Alpha-Beta algoritms)
    def makeMovePC(self):
        if self.game_over:
            return

        available_indx = [i for i, x in enumerate(self.array_of_numbers) if x is not None]

        if not available_indx:
            self.gui.set_buttons_state("normal")
            return

        # Šeit izveido pašreizējo spēles stāvokli
        current_state = SpecificState(
            sequence=self.array_of_numbers,
            human_points=self.human_points,
            computer_points=self.computer_points,
            current_player="Dators",
        )

        # Šeit izveido atbilstošo koka mezglu balstoties uz izveidoto stāvokli "current_state"
        root_node = SpecificTreeNode(current_state)
        # Šeit tiek ierobežots dzilums, un tiek izvēlets minimālais starp noklusēto 4
        # vai ja pieejamie indeksi ir mazāk, tad izvēlas to
        tree_depth = min(4, len(available_indx))
        # Tiek padoti dati un saģenerēts nepilns koks
        makeTree(root_node, tree_depth)

        start_time = time.perf_counter()

        # izmanto izvēlēto algoritmu, lai atrastu labāko gājienu
        if self.settings["algoritms"] == "Alpha-Beta":
            _, best_move, _ = AlphaBetaAlgo(root_node, -999999, 999999)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(f"{elapsed_time_microseconds:.2f}")

        else:
            _, best_move, _ = MinMaxAlgo(root_node)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(f"{elapsed_time_microseconds:.2f}")

        # ja minimax neatrada gājienu, izvēlas nejaušu
        if best_move is None:
            print("DEBUG random choice made")
            best_move = random.choice(available_indx)

        self.MakeMoveGUI(best_move)
        self.gui.set_buttons_state("normal")

    # Nosaka un paziņo uzvarētāju
    def chooseWinner(self):
        if self.human_points < self.computer_points:
            self.gui.show_winner("Cilvēkam UZVARA! Cilvēkam mazāk punktu!", "cyan")
        elif self.computer_points < self.human_points:
            self.gui.show_winner("Cilvēkam ZAUDĒJUMS! Datoram mazāk punktu!", "red")
        else:
            self.gui.show_winner("NEIZŠĶIRTS!", "yellow")

    # Palaiž Tkinter logu
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    speles_dzinis = GameLogic()
    speles_dzinis.run()
