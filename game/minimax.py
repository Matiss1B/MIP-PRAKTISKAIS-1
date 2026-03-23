
from game.hier_func import heirFunc


def r_print(node, ident=0):
    print(f"{' ' * ident}Mezgls: {node.state} | Gājiens: {node.index}")
    for child in node.children:
        ident += 2
        r_print(child, ident)


def MinMaxAlgo(node):
    # Pārbauda vai pēcteču sakits nav viendāds ar nulli, kā arī vai spēle nav beigusies, ja
    # Ja spēle ir beigusies, funkcija beidz darbību
    if len(node.children) == 0 or node.state.gameOverState():
        # Pielieto heiristisko funkciju lai novērtētu konkrēto gajienu,
        # ja tiktu izvveleta virsotne
        score = heirFunc(node.state)
        # Atgriež vērtību gājienam,
        # atgriež konkrēto gājiena/izvēlētā skaitļa indeksu,
        # atgriež apskatīto virsotņu skaitu
        return score, node.index, 1
    # Tiek skaitīts apskatīto virsotņu skaits, sākotnēji piešķirot0
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
            child_score, _, evaluated = MinMaxAlgo(child)

            evaluatedNodesCount += evaluated
            # Ja šis konkrētais gājiens ir
            # tas tiek iestatīts kā labākais gājiens un
            # ayjauno labāko punktu skaitu
            if child_score > best_score:
                best_score = child_score
                best_move = child.index

        return best_score, best_move, evaluatedNodesCount
    else:
        # Ja spēlē cilvēks tas minimizē,
        # tapēc ir iestatīta maksimāli liela vērtība
        best_score = 999999
        # Saglabā labāko gājienu
        best_move = None
        # Arī apskata visus iespējamos gājienus
        for child in node.children:
            # rekursīvi izsauc šo funkciju arī bernam
            child_score, _, evaluated = MinMaxAlgo(child)
            evaluatedNodesCount += evaluated
            # Ja novērtējuma punkti ir mazāki,
            # tad tas gajiens labāks minimizētājam,
            # un tiek iestatīts kā labākais gājiens
            if child_score < best_score:
                best_score = child_score
                best_move = child.index

        return best_score, best_move, evaluatedNodesCount
