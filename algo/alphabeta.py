from hier_func import evaluate


def alphabeta(node, alpha, beta):
    # Leaf node: no children (tree depth limit reached) or game is over
    if len(node.children) == 0 or node.state.is_game_over():
        score = evaluate(node.state)
        return score, node.move_index, 1

    total_evaluated = 0

    # max - player (Dators)
    if node.state.current_player == "Dators":
        best_score = -999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = alphabeta(child, alpha, beta)
            total_evaluated += evaluated

            if child_score > best_score:
                best_score = child_score
                best_move = child.move_index

            # Update alpha
            if best_score > alpha:
                alpha = best_score

            # Beta cutoff: minimizer would never allow this branch
            if alpha >= beta:
                break

        return best_score, best_move, total_evaluated

    # min - cilveks
    else:
        best_score = 999999
        best_move = None

        for child in node.children:
            child_score, _, evaluated = alphabeta(child, alpha, beta)
            total_evaluated += evaluated

            if child_score < best_score:
                best_score = child_score
                best_move = child.move_index

            # Update beta
            if best_score < beta:
                beta = best_score

            # Alpha cutoff: maximizer would never allow this branch
            if alpha >= beta:
                break

        return best_score, best_move, total_evaluated
