#!/bin/bash

# 检查 .env.avatar 文件是否存在
if [ -f .env.avatar ]; then
    # 复制 .env.avatar 为 .env
    echo "正在复制 .env.avatar 为 .env..."
    cp .env.avatar .env

    # 提示复制成功
    echo "复制完成！已将 .env.avatar 文件复制为 .env。"
else
    # 提示 .env.avatar 文件不存在
    echo "无法找到 .env.avatar 文件。"
fi

# 读取 .env 文件中的 DOMAIN_NAME
echo "正在读取 .env 文件..."
if [[ -f .env ]]; then
    source .env
    echo "成功读取 .env 文件。"
else
    echo "无法找到 .env 文件。脚本执行终止。"
    exit 1
fi

echo "正在安装系统依赖以及升级系统..."

sudo apt-get update -y
sudo apt-get install software-properties-common -y
sudo add-apt-repository universe -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update -y

# 检查 MySQL 是否已安装
if ! command -v mysql &> /dev/null; then
    echo "MySQL 未安装，开始执行安装脚本..."

    # 自动安装 MySQL
    echo "正在安装 MySQL..."
    yes | sudo apt-get install mysql-server

    # 安装完成后的提示信息
    echo "MySQL 安装完成！"
else
    echo "MySQL 已安装，跳过安装过程。"
fi

if [[ -n "$DB_PASSWORD" ]]; then
    # 创建数据库和用户
    echo "正在创建数据库和用户..."
    sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS avatar;
USE avatar;

CREATE USER 'master'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON avatar.* TO 'master'@'localhost';
FLUSH PRIVILEGES;

EOF
fi
echo "用户 'master' 创建成功！"

# Restore db_cmc_total_supply.sql
mysql -u root avatar < /root/tg/files/db_backup/db_cmc_total_supply.sql

# Restore db_daily_words.sql
mysql -u root avatar < /root/tg/files/db_backup/db_daily_words.sql

echo "Mysql 数据库表单 db_cmc_total_supply, db_daily_words 导入成功"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed, starting the installation process..."
    
    # Download Anaconda installation script
    echo "Downloading Anaconda installation script..."
    curl -o anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh

    # Execute Anaconda installation script (automatically confirm if prompted)
    echo "Executing Anaconda installation script..."
    bash anaconda.sh -b -p $HOME/anaconda3

    # Prompt to initialize conda
    echo "Do you want to initialize conda? (yes/no)"
    read -r initialize_conda

    if [[ $initialize_conda == "yes" ]]; then
        # Initialize conda
        echo "Initializing conda..."
        source $HOME/anaconda3/etc/profile.d/conda.sh
        conda init bash
    fi

    # Clean up temporary files
    echo "Cleaning up temporary files..."
    rm anaconda.sh

    # Display installation completion message
    echo "Anaconda installation completed!"
fi

# Check if the 'av' virtual environment is created
if conda env list | grep -q "av"; then
    echo "The 'av' virtual environment already exists. Skipping environment creation process."
else
    # Create the 'av' virtual environment
    echo "Creating the 'av' virtual environment..."
    conda create -y -n av python=3.9

    # Display virtual environment creation success message
    echo "The 'av' virtual environment has been created successfully!"
fi


# Export the PATH variable
export PATH=/root/anaconda3/bin:$PATH

# 结束脚本
echo "自动部署 Auto Deployment 脚本 1/4 执行结束。请退出 Terminal 并重新登录， 然后用 cav aliases 进入虚拟环境 av, 接着可以用 ccd aliases 命令安装 conda 以及 python 的依赖。"

