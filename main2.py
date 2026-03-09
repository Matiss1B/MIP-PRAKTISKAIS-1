from algo.minimax import minimax
from tree import TreeNode, build_tree


def minimax_decision(state, depth):
    root = TreeNode(state, move_index=None)

    nodes_generated = build_tree(root, depth)

    score, best_move, nodes_evaluated = minimax(root, depth)

    stats = {
        "genereti": nodes_generated,
        "apskatiti": nodes_evaluated,
    }

    return best_move, score, stats
