#!/bin/bash

# Define the base directory
base_dir="/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive"

# Define the source directory for rsync
source_dir="/Users/lgg/coding/preangelleo/crypto_assistant/tg"

# Use find command to list all the directories under the base directory
target_folder_name_list=$(find "$base_dir" -type d)

# Loop over each directory in the list
for folder_name in $target_folder_name_list
do
    # 检查 folder_name 是否是 '/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/wc', 如果不是则跳过
    if [ "$folder_name" != "/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/wc" ]; then
        continue
    fi
    
    # Check if the 'tg' folder exists within the current directory
    if [ ! -d "$folder_name/tg" ]; then
        # If not, skip to the next iteration of the loop
        continue
    fi

    # Use rsync to synchronize the source directory with the 'tg' folder in the current directory
    rsync -avz --exclude=".DS_Store" --exclude=".env" --exclude="__pycache__" --exclude="test_inlocal.py" --exclude="files/audio/clone_voice" --exclude="files/bing_search" --exclude=".chroma/" "$source_dir" "$folder_name"

    # 打开 folder_name 里面的 configuration.json , 读出 UBUNTU_SERVER_IP_ADDRESS 的值, rsync -avz --exclude=".DS_Store" "$folder_name/tg" root@UBUNTU_SERVER_IP_ADDRESS:/root/
    rsync -avz --exclude=".DS_Store" --exclude="__pycache__" --exclude="test_inlocal.py" --exclude="files/audio/clone_voice" --exclude="files/bing_search" --exclude=".chroma/" "$folder_name/tg" root@54.65.98.43:/root/
    # rsync -avz --exclude=".DS_Store" --exclude="__pycache__" --exclude="test_inlocal.py" --exclude="files/audio/clone_voice" "$folder_name/tg" root@$(cat "$folder_name/configuration.json" | jq -r '.UBUNTU_SERVER_IP_ADDRESS'):/root/

    # Connect to remote server
    # ssh -T root@$(cat "$folder_name/configuration.json" | jq -r '.UBUNTU_SERVER_IP_ADDRESS') << EOF
#     ssh -T root@54.65.98.43 << EOF

# # Change directory and activate conda environment
# cd /root/tg && conda activate av

# # Restart the pm2 process
# pm2 restart tg

# # Exit the remote server
# exit

# EOF

    # Print a success message
    echo "成功同步到: $(basename $folder_name) 文件夹"
done

