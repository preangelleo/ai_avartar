#!/bin/bash

echo "Stopping all pm2 programs..."
pm2 stop all

echo "Dropping binance_ltd_main database..."
mysql -u root -e "DROP DATABASE IF EXISTS binance_ltd_main;"
echo "Restoring binance_ltd_main database..."
mysql -u root -e "CREATE DATABASE binance_ltd_main;"
mysql -u root binance_ltd_main < /root/backup/binance_ltd_main.sql

echo "Starting all pm2 programs..."
pm2 start all

echo "Tables restore completed!"

# Loop through each table and get its size
mysql -u root -e "USE binance_ltd_main; SHOW TABLES;" | while read table; do
    size=$(mysql -u root -e "USE binance_ltd_main; SELECT ROUND(SUM(data_length + index_length)/1024/1024,2) AS 'Size (MB)' FROM information_schema.TABLES WHERE TABLE_NAME = '$table';" | awk 'NR==2 {print $1}')
    echo "  Table: $table (Size: $size MB)"
done

echo "Size of /var/lib/mysql/ibdata1: $(du -m /var/lib/mysql/ibdata1 | awk '{print $1}') MB"
