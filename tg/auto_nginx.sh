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

# 检查 DOMAIN_NAME 是否为空
if [[ -n "$DOMAIN_NAME" ]]; then
    # 安装 Nginx
    if ! command -v nginx &> /dev/null; then
        echo "Nginx 未安装，开始执行安装脚本..."

        # 自动安装 Nginx
        echo "正在安装 Nginx..."
        yes | sudo apt-get install nginx

        # 安装完成后的提示信息
        echo "Nginx 安装完成！"
    else
        echo "Nginx 已安装，跳过安装过程。"
    fi

    # 安装 Certbot
    if ! command -v certbot &> /dev/null; then
        echo "Certbot 未安装，开始执行安装脚本..."

        # 自动安装 Certbot
        echo "正在安装 Certbot..."
        yes | sudo apt-get install certbot

        # 安装完成后的提示信息
        echo "Certbot 安装完成！"
    else
        echo "Certbot 已安装，跳过安装过程。"
    fi

    # 使用 Certbot 获取 SSL 证书
    echo "正在获取 SSL 证书..."

    email="admin@$DOMAIN_NAME"
    echo "无法获取 SSL 证书，正在尝试使用电子邮件地址 $email..."
    if sudo certbot certonly --nginx -d "$DOMAIN_NAME" --register-unsafely-without-email --email "$email" --agree-tos; then
        echo "SSL 证书获取成功！( 使用电子邮件地址：$email )"
    else
        echo "无法获取 SSL 证书。请检查域名配置和 Certbot 设置。"
        exit 1
    fi

    # 更新 Nginx 默认配置文件
    echo "正在更新 Nginx 默认配置文件..."
    sudo sudo sed -i 's/listen 80;/listen 80;\n\trewrite ^ https:\/\/$host$request_uri permanent;/' /etc/nginx/sites-available/default

    # 创建 Nginx 配置文件
    echo "正在创建 Nginx 配置文件..."
    sudo tee /etc/nginx/sites-available/myapp.conf > /dev/null <<EOF
server {
    listen 80;
    listen [::]:80;

    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name $DOMAIN_NAME;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;

    location / {
proxy_pass http://localhost:3000;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
}
EOF

    # 创建符号链接
    echo "正在创建符号链接..."
    sudo ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/

    # 测试 Nginx 配置
    echo "正在测试 Nginx 配置..."
    if sudo nginx -t; then
        echo "Nginx 配置测试通过！"
    else
        echo "Nginx 配置测试失败。请检查配置文件语法。"
        exit 1
    fi

    # 重启 Nginx
    echo "正在重启 Nginx..."
    sudo service nginx restart

else
    echo "DOMAIN_NAME 为空。脚本执行终止。"
fi

echo "写入 Crontab 自动任务, 每天 0 点自动更新 SSL 证书..."
# Set the default editor to nano
export VISUAL=nano
export EDITOR=nano

# Run crontab with the -e option
crontab -e <<EOF
# Append the desired cron job entry here
0 0 * * * certbot renew --quiet >> /var/log/certbot-renew.log
EOF


# 结束脚本
echo "自动部署 Auto Deployment 脚本 4/4 执行结束，接下来可以用 bd, pd, pmtg, pmsw 等 aliases 命令执行程序。"
