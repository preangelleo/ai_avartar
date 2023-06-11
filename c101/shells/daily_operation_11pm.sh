#!/bin/bash

# Log the script start time
echo "Starting daily_operation_11pm.sh at $(date)"

# Change directory to the location of your Python script
cd /root/major

# Activate your Python environment with conda
/root/anaconda3/bin/conda activate env-major

# Run your Python script with the function
python3 c101operation.py
