#!/bin/bash

# 读取 .env 文件中的 DOMAIN_NAME
echo "正在读取 .env 文件..."
if [[ -f .env ]]; then
    source .env
    echo "成功读取 .env 文件。"
else
    echo "无法找到 .env 文件。脚本执行终止。"
    exit 1
fi

# 安装最新版的 nodejs, 如果遇到 prompt, 一律回复 yes 或者回车
echo "正在安装 nodejs..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 npm 如果遇到 prompt, 一律回复 yes 或者回车
echo "正在安装 npm..."
sudo apt-get install -y npm

# 安装 pnpm 如果遇到 prompt, 一律回复 yes 或者回车
echo "正在安装 pnpm..."
sudo npm install -g pnpm

# 安装 pm2 如果遇到 prompt, 一律回复 yes 或者回车
echo "正在安装 pm2..."
sudo npm install -g pm2


# 结束脚本
echo "自动部署 Auto Deployment 脚本 3/4 执行结束，接下来请用 pyi 初始化 Telegram Bot 然后用 pmtg 将 Bot 跑起来, 如果要部署 Website, 则用 cng 命令部署 Nginx 并通过 certbot 获取 SSL 证书。"

