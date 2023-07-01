#!/usr/bin/bash

export PATH="${PATH}:${HOME}/.local/bin:${HOME}/anaconda3/bin"
export PYTHONPATH="${PYTHONPATH}:${HOME}/ai_avartar"

cd /root/ai_avartar && conda activate av
cd /root
pm2 start ai_avartar/monitoring/fanbook_bot_monitor.py --name fanbook_bot_monitor --interpreter python3
