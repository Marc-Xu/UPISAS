import json
import random
from collections import defaultdict

from typing import Tuple

from UPISAS.strategy import Strategy


class QLearningAdaptation(Strategy):
    UPPER_THRESHOLD = -42
    LOWER_THRESHOLD = -48
    MIN_POWER = -1
    MAX_POWER = 15
    MIN_SF = 7
    MAX_SF = 12
    epsilon = 0

    def __init__(self, exemplar):
        super().__init__(exemplar)
        self.q_table = {}

        self.load_q_table()

    def save_q_table(self, file_path="q_table.json"):
        serializable_q_table = {str(state): actions for state, actions in self.q_table.items()}
        with open(file_path, "w") as file:
            json.dump(serializable_q_table, file)

    def load_q_table(self, file_path="q_table.json"):
        try:
            with open(file_path, "r") as file:
                serializable_q_table = json.load(file)
            # Convert string keys back to tuples
            self.q_table = {eval(state): actions for state, actions in serializable_q_table.items()}
        except FileNotFoundError:
            self.q_table = {}

    def analyze(self):
        data = self.knowledge.monitored_data
        mote_1 = data['moteStates'][-1][0]
        signal_strength = mote_1['highestReceivedSignal']
        packet_loss = mote_1['packetLoss']

        # Discretize signal strength into states
        if signal_strength > self.UPPER_THRESHOLD:
            signal_state = "high_signal"
        elif signal_strength < self.LOWER_THRESHOLD:
            signal_state = "low_signal"
        else:
            signal_state = "medium_signal"

        # Create state representation
        power = mote_1['transmissionPower']
        sf = mote_1['sf']
        state = (signal_state, power, sf)
        print(f"[Analyze]\tState: {state}, Packet Loss Rate: {packet_loss}")

        # Save state and packet loss rate for the plan phase
        self.knowledge.analysis_data['state'] = state
        self.knowledge.analysis_data['packet_loss'] = packet_loss
        return True

    @staticmethod
    def _plan_data(data: list[Tuple[str, int]]):
        return {
            "items": [
                {
                    "id": 0,
                    "adaptations": [
                        {
                            "name": name,
                            "value": value,
                        }
                        for name, value in data
                    ]
                },
            ]
        }

    # If this plan section is empty it will give an error:
    # ERROR:root:No complete JSON Schema provided for validation Keys misaligned
    def plan(self):
        state = self.knowledge.analysis_data['state']
        packet_loss = self.knowledge.analysis_data['packet_loss']
        signal_state, power, sf = state

        # Define actions
        actions = {
            "increase_power": lambda p, s: (min(p + 1, self.MAX_POWER), s),
            "decrease_power": lambda p, s: (max(p - 1, self.MIN_POWER), s),
            "increase_sf": lambda p, s: (p, min(s + 1, self.MAX_SF)),
            "decrease_sf": lambda p, s: (p, max(s - 1, self.MIN_SF)),
        }

        # Epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            new_action = random.choice(list(actions.keys()))  # Explore
        else:
            if state not in self.q_table:
                self.q_table[state] = {action: 0 for action in actions}
            new_action = max(self.q_table[state], key=self.q_table[state].get)  # Exploit

        # Apply action
        new_power, new_sf = actions[new_action](power, sf)
        print(f"[Plan]\tAction: {new_action}, New Power: {new_power}, New SF: {new_sf}")

        # Calculate reward
        energy_cost = power
        reward = 10 * (1 - packet_loss) - energy_cost
        print(f"[Plan]\tReward: {reward}")

        # Update Q-Table
        next_state = (signal_state, new_power, new_sf)
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0 for action in actions}
        max_future_q = max(self.q_table[next_state].values(), default=0)
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in actions}
        self.q_table[state][new_action] += 0.1 * (reward + 0.9 * max_future_q - self.q_table[state][new_action])
        print(self.q_table)

        # Update the plan data
        adjustments = [
            ("power", new_power),
            ("spreading_factor", new_sf),
        ]
        self.knowledge.plan_data = self._plan_data(adjustments)
        return True
