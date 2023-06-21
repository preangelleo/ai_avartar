# Set up prometheus monitoring with Grafana 

You need to config the instance IPv4 Firewall to allow access to

    3000 (for Grafana)
    9090 (for Prometheus)
    8000 (for bot's exported Prometheus metrics)

## Step 1: Set Up Prometheus
1. Install prometheus following https://prometheus.io/docs/prometheus/latest/getting_started/#getting-started;
2. Install prometheus_client and start_http_server in the same bot;
3. Run `/root/prometheus-2.45.0-rc.0.linux-amd64/prometheus --config.file=/root/ai_avartar/monitoring/prometheus.yml` so that prometheus will scrape the metrics exported in bots

## Step 2: Set Up Grafana 
Follow this [post](https://medium.com/devops-dudes/install-prometheus-on-ubuntu-18-04-a51602c6256b#:~:text=a%20web%20browser%3A-,Setting%20up%20Grafana%20For%20Prometheus,-First%2C%20Install%20Grafana)
1. Install Grafana Following https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/#install-from-apt-repository
2. Run `sudo systemctl daemon-reload && sudo systemctl enable grafana-server && sudo systemctl start grafana-server.service` to allow 
automatic start of Grafana by systemd
3. Goto `http://ip:3000` and link the Grafana to Prometheus in port 8000
