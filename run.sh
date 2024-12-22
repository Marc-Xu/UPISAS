#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/UPISAS
rm -r UPISAS/experiment_runner_configs/experiments
# run all experiments
python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/dingnet_all.py
# run baseline experiments
#python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/dingnet_baseline.py
# run signal based experiments
#python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/dingnet_signal_based.py
## run q-learning experiments
#python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/dingnet_q_learning.py
