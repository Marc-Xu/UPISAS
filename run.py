from UPISAS.strategies.dingnet_signal_based_strategy import SignalBasedAdaptation
from UPISAS.exemplars.dingnet import Dingnet
import sys
import time
import traceback

if __name__ == '__main__':
    
    exemplar = Dingnet(auto_start=True)
    time.sleep(20)
    exemplar.start_run()
    time.sleep(3)

    try:
        strategy = SignalBasedAdaptation(exemplar)

        strategy.get_monitor_schema()
        strategy.get_adaptation_options_schema()
        strategy.get_execute_schema()

        while True:
            input("Try to adapt?")
            strategy.monitor(verbose=True)
            if strategy.analyze():
                if strategy.plan():
                    strategy.execute()
            
    except (Exception, KeyboardInterrupt) as e:
        print("Traceback:")
        traceback.print_exc()  # Full traceback for debugging
        input("something went wrong")
        input("something went wrong")
        exemplar.stop_container()
        sys.exit(0)