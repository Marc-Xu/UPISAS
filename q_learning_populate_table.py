from UPISAS.strategies.dingnet_q_learning_strategy import QLearningAdaptation
from UPISAS.exemplars.dingnet import Dingnet
import sys
import time
import traceback

if __name__ == '__main__':
    
    exemplar = Dingnet(auto_start=True)
    time.sleep(20)
    exemplar.start_run()
    time.sleep(3)

    strategy = QLearningAdaptation(exemplar)

    strategy.get_monitor_schema()
    strategy.get_adaptation_options_schema()
    strategy.get_execute_schema()

    try:
        strategy.epsilon = 0.1
        for _ in range(100):
            time.sleep(3)
            strategy.monitor(verbose=True)
            if strategy.analyze():
                if strategy.plan():
                    strategy.execute()

    except (Exception, KeyboardInterrupt) as e:
        print("Traceback:")
        traceback.print_exc()  # Full traceback for debugging
        input("something went wrong, press enter to exit")
        strategy.save_q_table()
        exemplar.stop_container()
        sys.exit(0)

    strategy.save_q_table()
    exemplar.stop_container()
