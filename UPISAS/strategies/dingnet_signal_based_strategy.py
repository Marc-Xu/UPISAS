from UPISAS.strategy import Strategy


class SignalBasedAdaptation(Strategy):
    UPPER_THRESHOLD = -42
    LOWER_THRESHOLD = -48

    def analyze(self):
        lower_threshold = self.LOWER_THRESHOLD
        upper_threshold = self.UPPER_THRESHOLD
        data = self.knowledge.monitored_data
        mote_1 = data['moteStates'][0][0]
        signal_strength = mote_1['highestReceivedSignal']
        if signal_strength and not (lower_threshold < signal_strength < upper_threshold):
            print("[Analyze]\tSignal strength is poor, suggesting adaptation.")
            return True
        else:
            print("[Analyze]\tSignal strength is adequate, no adaptation needed.")
            return False

    # If this plan section is empty it will give an error:
    # ERROR:root:No complete JSON Schema provided for validation Keys misaligned
    def plan(self):
        self.knowledge.plan_data = {
            "items": [
                {
                    "id": 0,
                    "adaptations": [
                        {
                            "name": "power",
                            "value": 4
                        },
                    ]
                },
            ]
        }
        return True
