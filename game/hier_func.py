


def heirFunc(state):
    # Šeit tiek atņemts datora punktu skaiots no cilvēka punktiem,
    # kas ir heiristiskā novērtējuma funkcija,
    # jo lielāka atgriežamā vērtība, jo tas ir labāk datoram
    return state.human_points - state.computer_points
