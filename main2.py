from random import randint

from algo.minimax import minimax
from tree import GameState, TreeNode, build_tree


def doMinimax(state, depth):
    root = TreeNode(state, move_index=None)

    nodes_generated = build_tree(root, depth)

    score, best_move, nodes_evaluated = minimax(root, depth)

    stats = {
        "genereti": nodes_generated,
        "apskatiti": nodes_evaluated,
    }

    return best_move, score, stats


start = GameState(
    sequence=[randint(1, 10) for x in range(15)],
    human_points=100,
    computer_points=100,
    current_player="Dators",
)


def r_print(node, ident=0):
    # print(f"{' ' * ident}Mezgls: {node.state} | Gājiens: {node.move_index}")
    # for child in node.children:
    #     ident += 2
    #     r_print(child, ident)
    pass


root = TreeNode(start)
count = build_tree(root, depth=5)

# r_print(root)

best_move, score, stats = doMinimax(start, depth=5)
assert best_move is not None
chosen_value = start.sequence[best_move]

r_print(root)

print(f"best move: {best_move} (skaitlis {chosen_value})")
print(f"Score: {score}")
print(f"Mezgli ģenerēti: {stats['genereti']}")
print(f"Mezgli novērtēti: {stats['apskatiti']}")
