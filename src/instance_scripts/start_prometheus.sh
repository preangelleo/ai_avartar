#!/usr/bin/bash

cd /root
/root/prometheus-2.45.0-rc.0.linux-amd64/prometheus --config.file=/root/ai_avartar/monitoring/prometheus.yml --storage.tsdb.retention.time=365d --storage.tsdb.retention.size=1GB
