from game.hier_func import heirFunc


def AlphaBetaAlgo(node, alpha, beta):
    if len(node.children) == 0 or node.state.gameOverState():
        score = heirFunc(node.state)
        return score, node.index, 1
    evaluatedNodesCount = 0

    if node.state.current_player == "Dators":
        best_score = -999999
        best_move = None
        for child in node.children:
            child_score, _, evaluated = AlphaBetaAlgo(child, alpha, beta)
            evaluatedNodesCount += evaluated
            if child_score > best_score:
                best_score = child_score
                best_move = child.index

            if best_score > alpha:
                alpha = best_score

            if alpha >= beta:
                break

        return best_score, best_move, evaluatedNodesCount

    else:
        best_score = 999999
        best_move = None
        for child in node.children:
            child_score, _, evaluated = AlphaBetaAlgo(child, alpha, beta)
            evaluatedNodesCount += evaluated
            if child_score < best_score:
                best_score = child_score
                best_move = child.index

            if best_score < beta:
                beta = best_score

            if alpha >= beta:
                break

        return best_score, best_move, evaluatedNodesCount
