
class SpecificState:
    def __init__(self, sequence, human_points, computer_points, current_player):
        self.sequence = tuple(sequence)
        self.human_points = human_points
        self.computer_points = computer_points
        self.current_player = current_player

    def availableMoves(self):
        moves = []
        for i in range(len(self.sequence)):
            if self.sequence[i] is not None:
                moves.append(i)
        return moves

    def gameOverState(self):
        return not any(self.sequence)

    def makeMove(self, index):

        value = self.sequence[index]

        if value is None:
            raise ValueError(f"Pozīcijā {index} nav skaitļa (jau paņemts)!")

        new_human = self.human_points
        new_computer = self.computer_points
        if value % 2 == 0:
            penalty = value * 2
            if self.current_player == "Cilveks":
                new_human = new_human - penalty
            else:
                new_computer = new_computer - penalty
        else:
            if self.current_player == "Cilveks":
                new_computer = new_computer + value
            else:
                new_human = new_human + value

        new_sequence = list(self.sequence)
        new_sequence[index] = None
        if self.current_player == "Cilveks":
            next_player = "Dators"
        else:
            next_player = "Cilveks"

        return SpecificState(new_sequence, new_human, new_computer, next_player)


class SpecificTreeNode:

    def __init__(self, state, index=None):
        self.state = state
        self.index = index
        self.children = []


def makeTree(node, depth):
    nodes_created = 1
    if depth == 0 or node.state.gameOverState():
        return nodes_created
    available = node.state.availableMoves()
    for move in available:
        new_state = node.state.makeMove(move)
        child_node = SpecificTreeNode(new_state, index=move)
        node.children.append(child_node)
        nodes_created += makeTree(child_node, depth - 1)
    return nodes_created
