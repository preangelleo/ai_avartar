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


# 安装 python3-pip
echo "正在安装 python3-pip..."
yes | sudo apt-get install python3-pip

# 安装依赖包
echo "现在开始安装 Python 依赖包..."

# 安装 azure-cognitiveservices-speech
echo "正在安装 azure-cognitiveservices-speech..."
yes | pip install azure-cognitiveservices-speech

# 升级 azure-cognitiveservices-speech
echo "正在升级 azure-cognitiveservices-speech..."
yes | pip install --upgrade azure-cognitiveservices-speech

# 安装 pydub
echo "正在安装 pydub..."
yes | pip install pydub

# 安装 sqlalchemy
echo "正在安装 sqlalchemy..."
yes | pip install sqlalchemy

# 安装 langdetect
echo "正在安装 langdetect..."
yes | pip install langdetect

# 安装 pandas
echo "正在安装 pandas..."
yes | pip install pandas

# 安装 openai
echo "正在安装 openai..."
yes | pip install openai

# 安装 replicate
echo "正在安装 replicate..."
yes | pip install replicate

# 安装 langchain
echo "正在安装 langchain..."
yes | pip install langchain

# 安装 pinecone-client
echo "正在安装 pinecone-client..."
yes | pip install pinecone-client

# 安装 python-dotenv
echo "正在安装 python-dotenv..."
yes | pip install python-dotenv

# 安装 pymysql
echo "正在安装 pymysql..."
yes | pip install pymysql

# 安装 wolframalpha
echo "正在安装 wolframalpha..."
yes | pip install wolframalpha

# 安装 wikipedia
echo "正在安装 wikipedia..."
yes | pip install wikipedia

# 安装 xlrd
echo "正在安装 xlrd..."
yes | pip install xlrd

# 升级 pandas
echo "正在升级 pandas..."
yes | pip install --upgrade pandas

# 安装 build-essential、libssl-dev、ca-certificates、libasound2、wget
echo "正在安装 build-essential、libssl-dev、ca-certificates、libasound2、wget..."
yes | sudo apt-get install build-essential libssl-dev ca-certificates libasound2 wget

# 安装 ffmpeg
echo "正在安装 ffmpeg..."
yes | sudo apt-get install ffmpeg

# 安装 nginx
echo "正在安装 nginx..."
yes | sudo apt install nginx

# 安装 python3-certbot-nginx
echo "正在安装 python3-certbot-nginx..."
yes | sudo apt install python3-certbot-nginx

# 安装 chardet
echo "正在安装 chardet..."
yes | pip install chardet

# pip install cryptography
echo "正在安装 cryptography..."
yes | pip install cryptography

# pip install mnemonic
echo "正在安装 mnemonic..."
yes | pip install mnemonic

# pip install eth-account
echo "正在安装 eth-account..."
yes | pip install eth-account

# pip install web3
echo "正在安装 web3..."
yes | pip install web3

# pip install moralis
echo "正在安装 moralis..."
yes | pip install moralis

# pip install azure-core
echo "正在安装 azure-core..."
yes | pip install azure-core

echo "Python 依赖包安装完毕..."

# Function to change the server timezone
change_timezone() {
    echo "尝试修改服务器时区 timezone..."

    # Change to the desired timezone
    sudo cp -p /etc/localtime /etc/localtime-back
    sudo mv /etc/localtime /etc/localtime-back
    sudo ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

    echo "服务器时区已修改为本地时区"

    # Display the updated date and time
    date -R
}

# Rest of your script ...

# Call the function to change the timezone
change_timezone

# 结束脚本
echo "自动部署 Auto Deployment 脚本 2/4 执行结束， 接下来用 cnd aliases 命令安装 nodejs, npm, pnpm"

