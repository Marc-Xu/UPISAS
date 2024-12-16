#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/UPISAS
#rm -r UPISAS/experiment_runner_configs/experiments
# run all experiments
python3 experiment-runner/experiment-runner/ UPISAS/experiment_runner_configs/dingnet_all.py
