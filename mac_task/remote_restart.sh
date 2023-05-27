#!/bin/bash

# Define the base directory
base_dir="/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive"

# Define the source directory for rsync
source_dir="/Users/lgg/coding/preangelleo/ai_avartar/tg"

# Use find command to list all the directories under the base directory
target_folder_name_list=$(find "$base_dir" -type d)

# Loop over each directory in the list
for folder_name in $target_folder_name_list
do

    # 检查 folder_name 是否是 '/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/kk', 如果是则跳过
    if [ "$folder_name" == "/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/kk" ]; then
        continue
    fi

    # 检查 folder_name 是否是 '/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/yudun', 如果是则跳过
    if [ "$folder_name" == "/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive/yudun" ]; then
        continue
    fi

    # Check if the 'tg' folder exists within the current directory
    if [ ! -d "$folder_name/tg" ]; then
        # If not, skip to the next iteration of the loop
        continue
    fi

    # Connect to remote server
    ssh -T root@$(cat "$folder_name/configuration.json" | jq -r '.UBUNTU_SERVER_IP_ADDRESS') << EOF

# Change directory and activate conda environment
cd /root/tg && conda activate av

# Restart the pm2 process
pm2 restart tg

# Exit the remote server
exit

EOF

    # Print a success message
    echo "成功同步到: $(basename "$folder_name") 文件夹"
done

# Finish the job
echo "文件夹全部同步并且所有服务器均已重启成功."
