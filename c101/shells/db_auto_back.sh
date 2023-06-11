#!/bin/bash

set -euo pipefail

# Set up variables
DB_USER="root"
DB_NAME="binance_ltd_main"
BACKUP_DIR="/root/backup"

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate the backup filenames
DB_BACKUP_FILE="$BACKUP_DIR/$DB_NAME.sql"

echo "Backing up database..."
# Dump the entire MySQL database to a file
mysqldump -u "$DB_USER" "$DB_NAME" > "$DB_BACKUP_FILE"

# Check the size of /var/lib/mysql/ibdata1 and echo out with size in MB
SIZE=$(du -sm /var/lib/mysql/ibdata1 | cut -f1)
echo "Size of /var/lib/mysql/ibdata1 is ${SIZE}MB"
