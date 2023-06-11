#!/bin/bash
# $1 = target_file

scp -r /Users/lgg/anaconda3/envs/env-major/"$1" root@47.91.25.101:/root/major/"$2"

echo "Uploaded $1 to root@47.91.25.101:/root/major/$2"

