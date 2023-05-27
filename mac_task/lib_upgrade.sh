#!/bin/bash

# Check if the parameter is provided
if [ $# -eq 0 ]; then
    echo "Please provide a parameter."
    exit 1
fi

# Assign the parameter to a variable
target_folder="$1"

# Define the base directory
base_dir="/Users/lgg/Downloads/Create_AI_Avatar/Users_Archive"

# Define the source directory for rsync
source_dir="/Users/lgg/coding/preangelleo/ai_avartar/tg"

# Use find command to list all the directories under the base directory
target_folder_name_list=$(find "$base_dir" -type d)

# Loop over each directory in the list
for folder_name in $target_folder_name_list
do
#
    if [ "$folder_name" != "$base_dir/$target_folder" ]; then
        continue
    fi
    
    # Check if the 'tg' folder exists within the current directory
    if [ ! -d "$folder_name/tg" ]; then
        # If not, skip to the next iteration of the loop
        continue
    fi

    # Connect to remote server and execute commands
    ssh -T root@$(cat "$folder_name/configuration.json" | jq -r '.UBUNTU_SERVER_IP_ADDRESS') << EOF

sudo apt-get update -y
sudo apt-get upgrade -y

# Exit the remote server
exit

EOF

    # Print a success message
    echo "成功同步到: $(basename "$folder_name") 文件夹"
done
