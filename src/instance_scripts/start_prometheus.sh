#!/usr/bin/bash

cd /home/ubuntu
/home/ubuntu/prometheus-2.46.0.linux-amd64/prometheus --config.file=/home/ubuntu/ai_avartar/monitoring/prometheus.yml --storage.tsdb.retention.time=365d --storage.tsdb.retention.size=1GB
