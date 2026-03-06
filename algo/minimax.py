
#   1. GameState  — viens "stāvoklis" spēlē (kas notiek TIEŠI TAGAD)
#   2. TreeNode   — viens "mezgls" kokā (satur stāvokli + bērnu mezglus)
#   3. build_tree — funkcija, kas ģenerē koku līdz noteiktam dziļumam
#   4. evaluate   — heiristiskā funkcija (novērtē, cik labs stāvoklis ir datoram)




# ------------------------------------------------------------
# 1. SPĒLES STĀVOKLIS (GameState)
# ------------------------------------------------------------
# Iedomājies, ka tu nofotografē spēli kādā brīdī.
# Foto redzams:
#   - kādi skaitļi vēl ir palikuši virknē
#   - cik punktu ir cilvēkam
#   - cik punktu ir datoram
#   - kurš tagad gājienu veic
# Tā ir GameState — viena "fotogrāfija" spēles brīdī.
# ------------------------------------------------------------


class GameState:
    """Viens spēles stāvoklis — 'fotogrāfija' no spēles brīža."""

    def __init__(self, sequence, human_points, computer_points, current_player):
        """
        Parametri:
            sequence       — skaitļu virkne, piemēram (2, None, 1, 4)
                             None nozīmē, ka skaitlis jau ir paņemts
            human_points   — cilvēka punkti (sākumā 100)
            computer_points— datora punkti (sākumā 100)
            current_player — kurš tagad spēlē: "Cilveks" vai "Dators"
        """
        # Saglabājam virkni kā tuple (nevar mainīt nejauši)
        self.sequence = tuple(sequence)
        self.human_points = human_points
        self.computer_points = computer_points
        self.current_player = current_player

    def get_available_moves(self):
        """
        Atgriež sarakstu ar indeksiem, kur vēl ir skaitļi (nav None).

        Piemērs:
            sequence = (2, None, 1, 4)
            Rezultāts: [0, 2, 3]   (pozīcijā 1 ir None, tāpēc to izlaižam)
        """
        moves = []
        for i in range(len(self.sequence)):
            if self.sequence[i] is not None:
                moves.append(i)
        return moves

    def is_game_over(self):
        """
        Pārbauda, vai spēle ir beigusies (visi skaitļi ir paņemti).

        Piemērs:
            (None, None, None) → True  (viss paņemts, spēle beigusies)
            (None, 3, None)    → False (vēl var spēlēt)
        """
        for value in self.sequence:
            if value is not None:
                return False  # Atradu skaitli — spēle turpinās
        return True  # Neviena skaitļa nav — spēle beigusies

    def make_move(self, index):
        """
        Izveido JAUNU stāvokli pēc gājiena (paņemot skaitli pozīcijā 'index').
        Pašreizējo stāvokli NEMAINA — vienmēr atgriež jaunu.

        Parametri:
            index — kuru skaitli paņemt (pozīcija virknē)

        Piemērs:
            Stāvoklis: sequence=(2, 1, 4), human=100, computer=100, player="Dators"
            Gājiens: index=0 (paņem skaitli 2)
            Skaitlis 2 ir PĀRA → no Datora punktiem atņem 2*2=4
            Jauns stāvoklis: sequence=(None, 1, 4), human=100, computer=96, player="Cilveks"
        """
        value = self.sequence[index]

        # Pārbaudām, vai šī pozīcija nav jau tukša
        if value is None:
            raise ValueError(f"Pozīcijā {index} nav skaitļa (jau paņemts)!")

        # Sākam ar pašreizējiem punktiem
        new_human = self.human_points
        new_computer = self.computer_points

        # --- NOTEIKUMU PIEMĒROŠANA ---

        if value % 2 == 0:
            # PĀRA skaitlis (2 vai 4): no SAVA punktu skaita atņem skaitlis * 2
            penalty = value * 2
            if self.current_player == "Cilveks":
                new_human = new_human - penalty
            else:
                new_computer = new_computer - penalty
        else:
            # NEPĀRA skaitlis (1 vai 3): PRETINIEKAM pieskaita šo skaitli
            if self.current_player == "Cilveks":
                new_computer = new_computer + value
            else:
                new_human = new_human + value

        # --- JAUNĀS VIRKNES IZVEIDOŠANA ---
        # Kopējam virkni un aizstājam paņemto skaitli ar None
        new_sequence = list(self.sequence)  # tuple → list (lai var mainīt)
        new_sequence[index] = None  # Izdzēšam paņemto skaitli

        # --- SPĒLĒTĀJA MAIŅA ---
        if self.current_player == "Cilveks":
            next_player = "Dators"
        else:
            next_player = "Cilveks"

        # Atgriežam JAUNU stāvokli (vecais paliek nemainīts!)
        return GameState(new_sequence, new_human, new_computer, next_player)

    def __repr__(self):
        """Lai varētu izdrukāt stāvokli ar print() — ērti testēšanai."""
        nums = [str(x) if x is not None else "_" for x in self.sequence]
        return (
            f"Virkne: [{', '.join(nums)}] | "
            f"Cilvēks: {self.human_points} | "
            f"Dators: {self.computer_points} | "
            f"Spēlē: {self.current_player}"
        )


# ------------------------------------------------------------
# 2. KOKA MEZGLS (TreeNode)
# ------------------------------------------------------------
# Iedomājies koku ar zariem:
#   - Sakne (root) ir pašreizējais stāvoklis
#   - Katrs zars ir viens iespējamais gājiens
#   - Katra zara galā ir jauns mezgls ar jaunu stāvokli
#
# Piemērs ar virkni [2, 1]:
#
#          [2, 1] H=100 C=100 (Dators spēlē)     ← SAKNE
#          /                    \
#    paņem 2                   paņem 1
#    [_, 1] H=100 C=96       [2, _] H=101 C=100   ← BĒRNI
#      |                       |
#    paņem 1                 paņem 2
#    [_, _] H=101 C=96      [_, _] H=97 C=100     ← MAZBĒRNI
# ------------------------------------------------------------


class TreeNode:
    """Viens mezgls spēles kokā."""

    def __init__(self, state, move_index=None):
        """
        Parametri:
            state      — GameState objekts (kas notiek šajā mezglā)
            move_index — kurš gājiens noveda uz šo mezglu (None saknei)
        """
        self.state = state  # Stāvoklis šajā mezglā
        self.move_index = move_index  # Kāds gājiens tika izdarīts, lai šeit nonāktu
        self.children = []  # Bērnu mezglu saraksts (sākumā tukšs)


# ------------------------------------------------------------
# 3. KOKA ĢENERĒŠANA (build_tree)
# ------------------------------------------------------------
# Šī funkcija no viena mezgla izveido visu koku līdz noteiktam dziļumam.
#
# Kāpēc ir dziļuma ierobežojums?
#   Ja virknē ir 20 skaitļi, pilns koks būtu 20! = ~2.4 kvintiljoni mezglu.
#   Tas neietilpst ne atmiņā, ne laika gaitā.
#   Tāpēc mēs ģenerējam tikai dažus līmeņus uz priekšu (piemēram, 4-6).
# ------------------------------------------------------------


def build_tree(node, depth):
    """
    Rekursīvi ģenerē spēles koku, sākot no 'node', līdz dziļumam 'depth'.

    Parametri:
        node  — TreeNode, no kura sākam ģenerēt
        depth — cik līmeņus vēl ģenerēt (0 = neģenerē bērnus)

    Atgriež:
        Cik mezglu tika izveidoti (lai varētu ziņot statistiku eksperimentos).

    Kā tas strādā:
        1. Ja depth=0 vai spēle beigusies → neģenerē bērnus, atgriež 1 (pats mezgls)
        2. Citādi: katram iespējamam gājienam:
           a) Izveido jaunu stāvokli (make_move)
           b) Izveido jaunu bērna mezglu
           c) Pievieno bērnu pašreizējā mezgla children sarakstam
           d) Rekursīvi ģenerē bērna apakškoku (depth - 1)
    """
    nodes_created = 1  # Ieskaitām pašu šo mezglu

    # Apstāšanās nosacījumi:
    # - depth == 0: sasniedzām maksimālo dziļumu
    # - is_game_over(): virkne ir tukša, nav ko spēlēt
    if depth == 0 or node.state.is_game_over():
        return nodes_created

    # Atrodam visus iespējamos gājienus (indeksus, kur vēl ir skaitļi)
    available = node.state.get_available_moves()

    for move in available:
        # 1. Izpildām gājienu un iegūstam jaunu stāvokli
        new_state = node.state.make_move(move)

        # 2. Izveidojam jaunu mezglu ar šo stāvokli
        child_node = TreeNode(new_state, move_index=move)

        # 3. Pievienojam mezglu kā bērnu
        node.children.append(child_node)

        # 4. Rekursīvi ģenerējam bērna apakškoku (vienu līmeni mazāk)
        nodes_created += build_tree(child_node, depth - 1)

    return nodes_created


# ------------------------------------------------------------
# 4. HEIRISTISKĀ FUNKCIJA (evaluate)
# ------------------------------------------------------------
# Kad koks ir uzbūvēts un mēs nonākam pie "lapas" (leaf — mezgls
# bez bērniem), mums jānovērtē: cik labs šis stāvoklis ir DATORAM?
#
# Ideja: Dators grib, lai VIŅAM būtu MAZĀK punktu.
#        Tātad, jo LIELĀKA starpība (cilvēka punkti - datora punkti),
#        jo LABĀK datoram.
#
# Piemērs:
#   Cilvēks: 105, Dators: 90 → score = 105 - 90 = +15  (LABI datoram)
#   Cilvēks: 90, Dators: 105 → score = 90 - 105 = -15  (SLIKTI datoram)
#   Cilvēks: 100, Dators: 100 → score = 0               (VIENĀDI)
# ------------------------------------------------------------


def evaluate(state):
    """
    Novērtē stāvokli no DATORA skatpunkta.

    Pozitīvs skaitlis = labi datoram (cilvēkam vairāk punktu)
    Negatīvs skaitlis = slikti datoram (datoram vairāk punktu)
    Nulle = vienādi
    """
    return state.human_points - state.computer_points


