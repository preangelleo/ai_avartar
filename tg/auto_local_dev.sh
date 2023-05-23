#!/bin/bash

# 先把服务器上的代码 Git 到本地
# 从自己的 Bot 服务器上把 .env 文件下载到项目文件夹下

# 读取 .env 文件
echo "正在读取 .env 文件..."
if [[ -f .env ]]; then
    source .env
    echo "成功读取 .env 文件。"
else
    echo "无法找到 .env 文件。脚本执行终止。"
    exit 1
fi

echo "正在安装系统依赖以及升级系统..."

# 检查 MySQL 是否已安装
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed, starting the installation process..."

    # Automatically install MySQL using Homebrew
    echo "Installing MySQL..."
    brew install mysql

    # Start the MySQL service
    echo "Starting MySQL service..."
    brew services start mysql

    # Display installation completion message
    echo "MySQL installation completed!"
else
    echo "MySQL is already installed. Skipping the installation process."
fi

echo "brew install ffmpeg"
brew install ffmpeg

echo '''
自行进入 MySQL 命令行，输入以下命令创建数据库和用户, master 密码默认是 uCwp3DdtZLazbjkS 如果想改就改好再执行以下代码:

CREATE DATABASE IF NOT EXISTS avatar;
USE avatar;
CREATE USER 'master'@'localhost' IDENTIFIED BY 'uCwp3DdtZLazbjkS';
GRANT ALL PRIVILEGES ON avatar.* TO 'master'@'localhost';
FLUSH PRIVILEGES;'''

echo "用户 'master' 创建成功！接下来请 cd 到项目文件夹再操作以下命令"

# Restore db_cmc_total_supply.sql
mysql -u root -p avatar < files/db_backup/db_cmc_total_supply.sql

# Restore db_daily_words.sql
mysql -u root -p avatar < files/db_backup/db_daily_words.sql

echo "Mysql 数据库表单 db_cmc_total_supply, db_daily_words 导入成功"

echo '''
接下来请手动执行以下命令安装 python 依赖:

1）进入项目文件夹
2）conda create -n tg
3）conda activate tg
4）pip install -r requrements.txt
5）pip install --upgrade azure-cognitiveservices-speech
6）pip install --upgrade pandas
'''


# 结束脚本
echo "数据库创建和导入成功, 请 pip install -r requirements.txt 安装 python 的依赖。"

