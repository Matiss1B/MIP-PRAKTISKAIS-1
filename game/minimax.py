from datetime import datetime

from game.hier_func import evaluate


def r_print(node, ident=0):
    print(f"{' ' * ident}Mezgls: {node.state} | Gājiens: {node.move_index}")
    for child in node.children:
        ident += 2
        r_print(child, ident)


def minimax(node):
    # Leaf node: no children (tree depth limit reached) or game is over
    if len(node.children) == 0 or node.state.is_game_over():
        score = evaluate(node.state)
        return score, node.move_index, 1

    total_evaluated = 0

    # if 'min' or 'max' level:
    if node.state.current_player == "Dators":
        best_score = -999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = minimax(child)
            total_evaluated += evaluated

            if child_score > best_score:
                best_score = child_score
                best_move = child.move_index

        return best_score, best_move, total_evaluated

    else:
        best_score = 999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = minimax(child)
            total_evaluated += evaluated

            if child_score < best_score:
                best_score = child_score
                best_move = child.move_index

        return best_score, best_move, total_evaluated
