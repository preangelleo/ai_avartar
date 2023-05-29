import os

DEAR_USER = '亲爱的'

system_prompt_backup_folder = 'files/system_prompt_backup'
sys_prompt_file_name = 'system_prompt.txt'
dialogue_tone_file_name = 'dialogue_tone.xls'
default_system_prompt_file = f'files/{sys_prompt_file_name}'
default_dialogue_tone_file = f'files/{dialogue_tone_file_name}'
system_prompt_backup_file = f'{system_prompt_backup_folder}/{sys_prompt_file_name}'
user_system_prompt_file = (
    default_system_prompt_file
    if os.path.isfile(default_system_prompt_file)
    else system_prompt_backup_file
)
