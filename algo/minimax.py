import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from hier_func import evaluate


def minimax(node, depth):
    if depth == 0 or node.state.is_game_over() or len(node.children) == 0:
        score = evaluate(node.state)
        return score, node.move_index, 1

    total_evaluated = 0

    if node.state.current_player == "Dators":
        best_score = -999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = minimax(child, depth - 1)
            total_evaluated += evaluated

            if child_score > best_score:
                best_score = child_score
                best_move = child.move_index

        return best_score, best_move, total_evaluated

    else:
        best_score = 999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = minimax(child, depth - 1)
            total_evaluated += evaluated

            if child_score < best_score:
                best_score = child_score
                best_move = child.move_index

        return best_score, best_move, total_evaluated
