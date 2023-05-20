import os
from PIL import Image

source_folder = '/Users/lgg/Downloads/Midjourney_remote'
sub_folders = {'1_vs_1': [], '1_vs_2': [], '3_vs_4': [], '4_vs_3': [], '2_vs_1': [], '9_vs_16': [], '16_vs_9': [], '3_vs_2': [], '2_vs_3': []}
ratios = {'1_vs_1': (1, 1), '1_vs_2': (1, 2), '3_vs_4': (3, 4), '4_vs_3': (4, 3), '2_vs_1': (2, 1), '9_vs_16': (9, 16), '16_vs_9': (16, 9), '3_vs_2': (3, 2), '2_vs_3': (2, 3)}

tolerance = 0.01

def move_image(file_path, sub_folder):
    destination = os.path.join(source_folder, sub_folder)
    if not os.path.exists(destination):
        os.makedirs(destination)
    os.rename(file_path, os.path.join(destination, os.path.basename(file_path)))

for file in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file)
    if file.endswith('.png'):
        with Image.open(file_path) as img:
            print(file_path)
            width, height = img.size
            for folder, ratio in ratios.items():
                calculated_ratio = float(width) / float(height)
                target_ratio = float(ratio[0]) / float(ratio[1])
                if abs(calculated_ratio - target_ratio) < tolerance:
                    move_image(file_path, folder)
                    break
