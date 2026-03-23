from game.hier_func import heirFunc


def AlphaBetaAlgo(node, alpha, beta):
    # Pārbauda vai pēcteču sakits nav viendāds ar nulli, kā arī vai spēle nav beigusies, ja
    # Ja spēle ir beigusies, funkcija beidz darbību
    if len(node.children) == 0 or node.state.gameOverState():
        # Pielieto heiristisko funkciju lai novērtētu konkrēto gajienu,
        # ja tiktu izvēleta virsotne
        score = heirFunc(node.state)
        # Atgriež vērtību gājienam,
        # atgriež konkrēto gājiena/izvēlētā skaitļa indeksu,
        # atgriež apskatīto virsotņu skaitu
        return score, node.index, 1
    # Tiek skaitīts apskatīto virsotņu skaits, sākotnēji piešķirot
    evaluatedNodesCount = 0

    if node.state.current_player == "Dators":
        # Spēli saķot datoram, tas cenšas maksimizēt, tāpēc
        # sākotnēja vērtiba iestatīta minimāla
        best_score = -999999
        # Saglabā labāko gājienu
        best_move = None
        # iziet cauri visiem iespējamajiem gājieniem
        for child in node.children:
            # rekursīvi izsauc šo funkciju arī bernam,
            # lai novertetu vairāk
            child_score, _, evaluated = AlphaBetaAlgo(child, alpha, beta)
            evaluatedNodesCount += evaluated
            # Ja šis konkrētais gājiens ir
            # tas tiek iestatīts kā labākais gājiens un
            # atjauno labāko punktu skaitu
            if child_score > best_score:
                best_score = child_score
                best_move = child.index

            # Tiek atjaunota alpha vertiba, labākais max vērtējums līdz šom
            if best_score > alpha:
                alpha = best_score

            # Šeit notiek konflikts, tiek nogriezts zars
            if alpha >= beta:
                break

        return best_score, best_move, evaluatedNodesCount

    else:
        # Ja spēlē cilvēks tas minimizē,
        # tapēc ir iestatīta maksimāli liela vērtība
        best_score = 999999
        # Saglabā labāko gājienu
        best_move = None
        # rekursīvi izsauc šo funkciju arī bernam
        for child in node.children:
            child_score, _, evaluated = AlphaBetaAlgo(child, alpha, beta)
            evaluatedNodesCount += evaluated
            # Ja šis konkrētais gājiens ir
            # tas tiek iestatīts kā labākais gājiens un
            # atjauno labāko punktu skaitu, tā kā spēlētajs minimize,
            # tas izvēlas minimalo vērtību kā labāko
            if child_score < best_score:
                best_score = child_score
                best_move = child.index

            # Tiek atjaunota alpha vertiba, labākais min vērtējums līdz šim
            if best_score < beta:
                beta = best_score

            # Šeit notiek konflikts, tiek nogriezts zars
            if alpha >= beta:
                break

        return best_score, best_move, evaluatedNodesCount
