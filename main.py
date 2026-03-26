import random
import time
import tkinter as tk
import csv
import os

from game.alphabeta import AlphaBetaAlgo
from game.minimax import MinMaxAlgo
from gui.main_gui import GameGUI
from game.tree import SpecificState, SpecificTreeNode, makeTree

def count_nodes(node):
    total = 1
    for child in node.children:
        total += count_nodes(child)
    return total


class GameLogic:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = GameGUI(self.root)

        self.gui.on_start_game = self.StartTheGame
        self.gui.on_number_clicked = self.MakeMoveGUI

        self.human_points = 100
        self.computer_points = 100
        self.array_of_numbers = []
        self.active_player = None
        self.settings = {}
        self.game_over = False
        self.experiment_data = []
        self.current_game_times = []
        self.current_game_generated_nodes = []
        self.current_game_evaluated_nodes = []

    def StartTheGame(self, settings):
        self.settings = settings
        self.human_points = 100
        self.computer_points = 100
        self.game_over = False
        self.active_player = settings["sacejs"]

        self.current_game_times = []
        self.current_game_generated_nodes = []
        self.current_game_evaluated_nodes = []

        lenght_of_array = settings["garums"]
        self.array_of_numbers = [random.randint(1, 4) for _ in range(lenght_of_array)]

        self.gui.build_game_board(
            self.array_of_numbers, self.active_player, settings["algoritms"], lenght_of_array
        )

        if self.active_player == "Dators":
            self.startPCTurn()

    def MakeMoveGUI(self, index):
        if self.game_over or self.array_of_numbers[index] is None:
            return

        number = self.array_of_numbers[index]

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

        self.array_of_numbers[index] = None
        self.gui.update_scores(self.human_points, self.computer_points)
        self.gui.remove_button(index)

        if all(x is None for x in self.array_of_numbers):
            self.game_over = True
            self.chooseWinner()
            return

        self.active_player = (
            "Dators" if self.active_player == "Cilveks" else "Cilveks"
        )
        self.gui.update_turn_indicator(self.active_player)

        if self.active_player == "Dators":
            self.startPCTurn()

    def startPCTurn(self):
        self.gui.set_buttons_state("disabled")
        self.root.after(800, self.makeMovePC)

    def makeMovePC(self):
        if self.game_over:
            return

        available_indx = [i for i, x in enumerate(self.array_of_numbers) if x is not None]

        if not available_indx:
            self.gui.set_buttons_state("normal")
            return

        current_state = SpecificState(
            sequence=self.array_of_numbers,
            human_points=self.human_points,
            computer_points=self.computer_points,
            current_player="Dators",
        )

        root_node = SpecificTreeNode(current_state)
        tree_depth = min(4, len(available_indx))
        makeTree(root_node, tree_depth)

        generated_nodes = count_nodes(root_node)

        start_time = time.perf_counter()

        if self.settings["algoritms"] == "Alpha-Beta":
            _, best_move, evaluated_nodes = AlphaBetaAlgo(root_node, -999999, 999999)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(
                f"Algoritms: Alpha-Beta | Laiks (μs): {elapsed_time_microseconds:.2f}"
            )

        else:
            _, best_move, evaluated_nodes = MinMaxAlgo(root_node)
            end_time = time.perf_counter()
            elapsed_time_microseconds = (end_time - start_time) * 1_000_000
            print(
                f"Algoritms: Minimax | Laiks (μs): {elapsed_time_microseconds:.2f}"
            )

        self.current_game_times.append(elapsed_time_microseconds)
        self.current_game_generated_nodes.append(generated_nodes)
        self.current_game_evaluated_nodes.append(evaluated_nodes)

        print(f"Ģenerētās virsotnes: {generated_nodes}")
        print(f"Novērtētās virsotnes: {evaluated_nodes}")

        if best_move is None:
            print("DEBUG random choice made")
            best_move = random.choice(available_indx)

        self.MakeMoveGUI(best_move)
        self.gui.set_buttons_state("normal")

    def chooseWinner(self):
        if self.human_points < self.computer_points:
            winner = "Cilvēks"
            self.gui.show_winner("Cilvēkam UZVARA! Cilvēkam mazāk punktu!", "cyan")
        elif self.computer_points < self.human_points:
            winner = "Dators"
            self.gui.show_winner("Cilvēkam ZAUDĒJUMS! Datoram mazāk punktu!", "red")
        else:
            winner = "Neizšķirts"
            self.gui.show_winner("NEIZŠĶIRTS!", "yellow")

        avg_time = (
            sum(self.current_game_times) / len(self.current_game_times)
            if self.current_game_times else 0
        )
        total_generated = sum(self.current_game_generated_nodes)
        total_evaluated = sum(self.current_game_evaluated_nodes)

        game_result = {
            "algoritms": self.settings["algoritms"],
            "sak_speletajs": self.settings["sacejs"],
            "virknes_garums": self.settings["garums"],
            "uzvaretajs": winner,
            "cilveka_punkti": self.human_points,
            "datora_punkti": self.computer_points,
            "videjais_datora_gajiena_laiks_us": avg_time,
            "genereto_virsotnu_skaits": total_generated,
            "noverteto_virsotnu_skaits": total_evaluated,
        }

        self.experiment_data.append(game_result)

        print("Spēles rezultāts:")
        print(game_result)

        file_exists = os.path.isfile("experiment_results.csv")

        with open("experiment_results.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "algoritms",
                    "sak_speletajs",
                    "virknes_garums",
                    "uzvaretajs",
                    "cilveka_punkti",
                    "datora_punkti",
                    "videjais_datora_gajiena_laiks_us",
                    "genereto_virsotnu_skaits",
                    "noverteto_virsotnu_skaits",
                ],
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(game_result)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    speles_dzinis = GameLogic()
    speles_dzinis.run()