
from game.hier_func import heirFunc


def r_print(node, ident=0):
    print(f"{' ' * ident}Mezgls: {node.state} | Gājiens: {node.index}")
    for child in node.children:
        ident += 2
        r_print(child, ident)


def MinMaxAlgo(node):
    if len(node.children) == 0 or node.state.gameOverState():
        score = heirFunc(node.state)
        return score, node.index, 1
    evaluatedNodesCount = 0

    if node.state.current_player == "Dators":
        best_score = -999999
        best_move = None
        for child in node.children:
            child_score, _, evaluated = MinMaxAlgo(child)

            evaluatedNodesCount += evaluated
            if child_score > best_score:
                best_score = child_score
                best_move = child.index

        return best_score, best_move, evaluatedNodesCount
    else:
        best_score = 999999
        best_move = None
        for child in node.children:
            child_score, _, evaluated = MinMaxAlgo(child)
            evaluatedNodesCount += evaluated
            if child_score < best_score:
                best_score = child_score
                best_move = child.index

        return best_score, best_move, evaluatedNodesCount
