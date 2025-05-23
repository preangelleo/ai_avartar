#!/usr/bin/bash

export PATH="${PATH}:${HOME}/.local/bin:${HOME}/anaconda3/bin"
export PYTHONPATH="${PYTHONPATH}:${HOME}/ai_avartar"

cd /ubuntu/ai_avartar && conda activate av
cd /root
pm2 start ai_avartar/src/bot/fanbook/fanbook_bot.py --name fb --interpreter python3
