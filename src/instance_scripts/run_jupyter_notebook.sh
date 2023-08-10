#!/usr/bin/bash

export PATH="${PATH}:/home/ubuntu/.local/bin"

cd /home/ubuntu/ai_avartar
jupyter notebook  --allow-root --ip 0.0.0.0  &>> /home/ubuntu/logs/jupyter_notebook/log.txt
