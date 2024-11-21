from UPISAS.strategy import Strategy

# This is a dummy strat for dingnet, with this it should be able to run, 
# when you are ready to implement your own strategy do it here.
class EmptyStrategy(Strategy):

    def analyze(self):

        data = self.knowledge.monitored_data
        mote_1 = data['moteStates'][0][0]
        spreading_factor = mote_1['sf']
        signal_strength = mote_1['highestReceivedSignal']
        if signal_strength and signal_strength < -48:
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
        }
    ]
    }
        return True