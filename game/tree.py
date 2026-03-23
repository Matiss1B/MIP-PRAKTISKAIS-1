
class SpecificState:
    def __init__(self, sequence, human_points, computer_points, current_player):
        # Šis glabā skaitļu virkni kas atrodas konkrētajā stāvoklī
        self.sequence = tuple(sequence)
        # Šis glabā cilvēka punktus
        self.human_points = human_points
        # Šis glabā datora punktus
        self.computer_points = computer_points
        # Šis glabā aktīvos spēlētāju
        self.current_player = current_player

    def availableMoves(self):
        # Šī funkcija atrgriez visus pieejamos gājienus,
        # kā tā indeksu no masīva jeb skaitļu virknes
        moves = []
        for i in range(len(self.sequence)):
            if self.sequence[i] is not None:
                moves.append(i)
        return moves

    def gameOverState(self):
        # Šī funkcija pārbauda vai spēle ir sasniegusio beigu stāvokli
        # ja virkne tukša tas atgriež false, savādāk true
        return not any(self.sequence)

    def makeMove(self, index):
       # Funkcija kas veic konkrēto datora gājienu

       # Šī ir gājienā izvēklētā vērtība
        value = self.sequence[index]

        # Drošības pēc tiek pārbaudīts vai nāv kļūme un nav izvēlēta tukša vērtība
        if value is None:
            raise ValueError(f"Pozīcijā {index} nav skaitļa (jau paņemts)!")

        # tiek inicializēti esošie punkti
        new_human = self.human_points
        new_computer = self.computer_points
        # Šajā sadaļā tiek izvērtēts ko darīt ar izvēletajiem skaitļiem un kā
        # mainīt punktus
        if value % 2 == 0:
            # Ja izvēlēts pāra skaitlis, tad tas tiek reizināts ar 2
            # un atņemts gājiena veicējam
            penalty = value * 2
            if self.current_player == "Cilveks":
                new_human = new_human - penalty
            else:
                new_computer = new_computer - penalty
        else:
            # Ja izvēlēts nepāra skaitlis, tad tiek pieskaitīts pretinieka punktiem
            if self.current_player == "Cilveks":
                new_computer = new_computer + value
            else:
                new_human = new_human + value

       # Šeit tiek dzēsts izvēlētais skaitlis un atjaunota spēles virkne
        new_sequence = list(self.sequence)
        new_sequence[index] = None
       # Šeit maina aktīvo spēlētāju
        if self.current_player == "Cilveks":
            next_player = "Dators"
        else:
            next_player = "Cilveks"

        # Šeit tiek atgriezts jauns stāvoklis pēc iegūtajiem datiem
        return SpecificState(new_sequence, new_human, new_computer, next_player)



class SpecificTreeNode:

    def __init__(self, state, index=None):
        # Šis ir konkrētais stāvoklis šajā mezglā
        self.state = state
        # Šis nosaka gājiena indeksu lai nonāktu līdz šim kokam
        self.index = index
        # Glabā bērnu skaitu
        self.children = []



def makeTree(node, depth):
    # Tiek skaitīts cik stāvokļi tiks saģenerēti, ieskaita pašreizējo stāvokli
    nodes_created = 1
    # Pārbauda vai dziļums nav viendāds ar nulli, kā arī vai spēle nav beigusies, ja
    # Ja spēle ir beigusies, funkcija beidz darbību
    if depth == 0 or node.state.gameOverState():
        return nodes_created
    # Atrodam visus iespējamos gājienus (indeksus, kur vēl ir skaitļi)
    available = node.state.availableMoves()
    for move in available:
        # Izpildām konkrēto gājienu un iegūstam jaunu stāvokli
        new_state = node.state.makeMove(move)
        # Izveidojam jaunu koka mezglu ar šo stāvokli
        child_node = SpecificTreeNode(new_state, index=move)
        # Pievienojam mezglu kā bērnu jau esošajam
        node.children.append(child_node)
        # Rekursīvi atkārtojam ģenerēšanu, bet to dara jau ar nākamo līmeni,
        # samazinot dziļumu
        nodes_created += makeTree(child_node, depth - 1)
    return nodes_created
