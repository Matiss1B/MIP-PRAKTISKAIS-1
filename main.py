import random
import time
import tkinter as tk

from game.alphabeta import alphabeta
from game.minimax import minimax
from gui.main_gui import GameGUI
from game.tree import GameState, TreeNode, build_tree


# Spēles loģikas un kontroles klase
class GameEngine:
    def __init__(self):
        # Izveido logu un piesaista GUI
        self.root = tk.Tk()
        self.gui = GameGUI(self.root)

        # Piesaista GUI pogas šī faila funkcijām
        self.gui.on_start_game = self.sakt_jaunu_speli
        self.gui.on_number_clicked = self.apstradat_gajienu

        # Spēles mainīgie
        self.cilveka_punkti = 100
        self.datora_punkti = 100
        self.virkne = []
        self.aktivais_speletajs = None
        self.iestatijumi = {}
        self.spele_beigusies = False

    # Sagatavo un sāk jaunu spēli
    def sakt_jaunu_speli(self, iestatijumi):
        self.iestatijumi = iestatijumi
        self.cilveka_punkti = 100
        self.datora_punkti = 100
        self.spele_beigusies = False
        self.aktivais_speletajs = iestatijumi["sacejs"]

        # Ģenerē skaitļu masīvu
        garums = iestatijumi["garums"]
        self.virkne = [random.randint(1, 4) for _ in range(garums)]

        self.gui.build_game_board(
            self.virkne, self.aktivais_speletajs, iestatijumi["algoritms"], garums
        )

        # Ja datori sāk pirmais, iedarbina tā gājienu
        if self.aktivais_speletajs == "Dators":
            self.sakt_datora_gajienu()

    # Apstrādā klikšķi (spēlētāja vai datora)
    def apstradat_gajienu(self, index):
        if self.spele_beigusies or self.virkne[index] is None:
            return

        skaitlis = self.virkne[index]

        # Punktu aprēķins
        if skaitlis % 2 == 0:
            atnem = skaitlis * 2
            if self.aktivais_speletajs == "Cilveks":
                self.cilveka_punkti -= atnem
            else:
                self.datora_punkti -= atnem
        else:
            if self.aktivais_speletajs == "Cilveks":
                self.datora_punkti += skaitlis
            else:
                self.cilveka_punkti += skaitlis

        # Atjauno GUI stāvokli
        self.virkne[index] = None
        self.gui.update_scores(self.cilveka_punkti, self.datora_punkti)
        self.gui.remove_button(index)

        # Pārbauda, vai spēle beigusies
        if all(x is None for x in self.virkne):
            self.spele_beigusies = True
            self.pazinot_uzvaretaju()
            return

        # Maina aktīvo spēlētāju
        self.aktivais_speletajs = (
            "Dators" if self.aktivais_speletajs == "Cilveks" else "Cilveks"
        )
        self.gui.update_turn_indicator(self.aktivais_speletajs)

        # Izsauc datora gājienu, ja nepieciešams
        if self.aktivais_speletajs == "Dators":
            self.sakt_datora_gajienu()

    # Nobloķē pogas un ieplāno datora gājienu
    def sakt_datora_gajienu(self):
        self.gui.set_buttons_state("disabled")
        self.root.after(800, self.veikt_datora_gajienu)

    # Datora loģika (Minimax vai Alpha-Beta algoritms)
    def veikt_datora_gajienu(self):
        if self.spele_beigusies:
            return

        pieejamie_indeksi = [i for i, x in enumerate(self.virkne) if x is not None]

        if not pieejamie_indeksi:
            self.gui.set_buttons_state("normal")
            return

        # izveido pašreizējo spēles stāvokli
        current_state = GameState(
            sequence=self.virkne,
            human_points=self.cilveka_punkti,
            computer_points=self.datora_punkti,
            current_player="Dators",
        )

        # izveido koka sakni un ģenerē koku
        root_node = TreeNode(current_state)
        tree_depth = min(4, len(pieejamie_indeksi))  # Ierobežo dziļumu
        build_tree(root_node, tree_depth)

        start_time = time.perf_counter()

        # izmanto izvēlēto algoritmu, lai atrastu labāko gājienu
        if self.iestatijumi["algoritms"] == "Alpha-Beta":
            _, best_move, _ = alphabeta(root_node, -999999, 999999)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(f"{elapsed_time_microseconds:.2f}")

        else:
            _, best_move, _ = minimax(root_node)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(f"{elapsed_time_microseconds:.2f}")

        # ja minimax neatrada gājienu, izvēlas nejaušu
        if best_move is None:
            print("DEBUG random choice made")
            best_move = random.choice(pieejamie_indeksi)

        self.apstradat_gajienu(best_move)
        self.gui.set_buttons_state("normal")

    # Nosaka un paziņo uzvarētāju
    def pazinot_uzvaretaju(self):
        if self.cilveka_punkti < self.datora_punkti:
            self.gui.show_winner("Cilvēkam UZVARA! Cilvēkam mazāk punktu!", "cyan")
        elif self.datora_punkti < self.cilveka_punkti:
            self.gui.show_winner("Cilvēkam ZAUDĒJUMS! Datoram mazāk punktu!", "red")
        else:
            self.gui.show_winner("NEIZŠĶIRTS!", "yellow")

    # Palaiž Tkinter logu
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    speles_dzinis = GameEngine()
    speles_dzinis.run()
