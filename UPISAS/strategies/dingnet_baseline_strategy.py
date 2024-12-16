from UPISAS.strategy import Strategy


class Baseline(Strategy):
    def analyze(self):
        return False

    # If this plan section is empty it will give an error:
    # ERROR:root:No complete JSON Schema provided for validation Keys misaligned
    def plan(self):
        return False
