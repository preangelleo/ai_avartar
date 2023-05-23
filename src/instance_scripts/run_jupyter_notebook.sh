#!/usr/bin/bash

export PATH="${PATH}:${HOME}/.local/bin:${HOME}/anaconda3/bin"

cd /root
jupyter notebook  --allow-root --ip 0.0.0.0  &>> /root/logs/jupyter_notebook/log.txt

