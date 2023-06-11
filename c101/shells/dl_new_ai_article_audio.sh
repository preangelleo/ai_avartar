#!/bin/bash

echo "Connecting to remote server..."
# SSH into the remote server and get the latest mp3 file
latest_file=$(ssh root@47.91.25.101 'ls -t /root/major/json_datas/sentences_tts/*.mp3 | head -1')
echo "Latest file on remote server: $latest_file"

# Get the filename of the latest file
filename=$(basename "$latest_file")
echo "Filename of latest file: $filename"

echo "Downloading latest file to local machine..."
# Download the latest file to the local machine
scp "root@47.91.25.101:/root/major/json_datas/sentences_tts/$filename" "/Users/lgg/Downloads/$filename"
echo "Downloaded $filename to /Users/lgg/Downloads"

# Print a message indicating the download is complete
echo "Download complete!"
