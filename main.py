from typing import Dict
import random


State = Dict[str, any];
def generate_start_state(number):
    return [random.randint(1,4) for _ in range(number)]

START_STATE: State = {
    "numbers" : generate_start_state(random.randint(15,25)),
    "computer_points": 100,
    "human_points": 100,

}
TERMINAL_STATE: State = {
    "numbers":[],
}
print(START_STATE, TERMINAL_STATE)

