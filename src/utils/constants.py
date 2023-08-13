import os

DEAR_USER = '亲爱的'

system_prompt_backup_folder = 'files/system_prompt_backup'
sys_prompt_file_name = 'system_prompt.txt'
dialogue_tone_file_name = 'dialogue_tone.xls'
default_system_prompt_file = f'files/{sys_prompt_file_name}'
default_dialogue_tone_file = f'files/{dialogue_tone_file_name}'
system_prompt_backup_file = f'{system_prompt_backup_folder}/{sys_prompt_file_name}'
user_system_prompt_file = (
    default_system_prompt_file if os.path.isfile(default_system_prompt_file) else system_prompt_backup_file
)

OPENAI_PRICE_MAP = {
    'gpt-4-0613': {'prompt_tokens': 0.00003, 'completion_tokens': 0.00006},
    'gpt-3.5-turbo-16k': {'prompt_tokens': 0.000003, 'completion_tokens': 0.000004},
    'gpt-3.5-turbo-16k-0613': {'prompt_tokens': 0.000003, 'completion_tokens': 0.000004},
    'gpt-3.5-turbo-0613': {'prompt_tokens': 0.0000015, 'completion_tokens': 0.000002},
}
