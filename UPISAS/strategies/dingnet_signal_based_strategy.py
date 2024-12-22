from UPISAS.strategy import Strategy


class SignalBasedAdaptation(Strategy):
    UPPER_THRESHOLD = -42
    LOWER_THRESHOLD = -48
    MIN_POWER = -1
    MAX_POWER = 15
    MIN_SF = 7
    MAX_SF = 12

    def analyze(self):
        data = self.knowledge.monitored_data
        mote_1 = data['moteStates'][-1][0]
        signal_strength = mote_1['highestReceivedSignal']
        if signal_strength and not (self.LOWER_THRESHOLD < signal_strength < self.UPPER_THRESHOLD):
            print("[Analyze]\tSignal strength is poor, suggesting adaptation.")
            self.knowledge.analysis_data['signal_strength'] = signal_strength
            self.knowledge.analysis_data['power'] = mote_1['transmissionPower']
            self.knowledge.analysis_data['sf'] = mote_1['sf']
            return True
        else:
            print("[Analyze]\tSignal strength is adequate, no adaptation needed.")
            return False

    # If this plan section is empty it will give an error:
    # ERROR:root:No complete JSON Schema provided for validation Keys misaligned
    def plan(self):
        signal_strength = self.knowledge.analysis_data['signal_strength']
        power = self.knowledge.analysis_data['power']
        spreading_factor = self.knowledge.analysis_data['sf']
        if signal_strength > self.UPPER_THRESHOLD:
            power += 1
            spreading_factor -= 1
        if signal_strength < self.LOWER_THRESHOLD:
            power -= 1
            spreading_factor += 1
        self.knowledge.plan_data = {
            "items": [
                {
                    "id": 0,
                    "adaptations": [
                        {
                            "name": "power",
                            "value": max(min(power, self.MAX_POWER), self.MIN_POWER)
                        },
                        {
                            "name": "spreading_factor",
                            "value": max(min(spreading_factor, self.MAX_SF), self.MIN_SF)
                        }
                    ]
                },
            ]
        }
        return True
