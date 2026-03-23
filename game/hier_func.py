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
