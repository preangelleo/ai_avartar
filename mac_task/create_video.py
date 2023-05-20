from main import *


def extract_audio(video_path, extension='.wav'):
    if extension == '.wav':
        audio_codec = 'pcm_s16le'
    elif extension == '.mp3':
        audio_codec = 'libmp3lame'
    else:
        raise ValueError("Unsupported audio format: {}".format(extension))
    audio_path = video_path[:-4] + extension
    cmd = ["ffmpeg", "-i", video_path, "-vn", "-acodec",
           audio_codec, "-ar", "44100", "-ac", "2", audio_path]
    subprocess.run(cmd, check=True)
    return audio_path


def merge_report_video(first_video_path, second_video_path):
    # Get the frame rate of the second video
    ffprobe_cmd = f"ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate {second_video_path}"
    second_video_framerate = subprocess.check_output(
        ffprobe_cmd, shell=True).decode("utf-8").strip()

    # Resize the first video to match the frame rate of the second video
    first_video_resized_path = os.path.splitext(first_video_path)[
        0] + "_resized.mp4"
    ffmpeg_resize_cmd = f"ffmpeg -i {first_video_path} -r {second_video_framerate} -c:v libx264 {first_video_resized_path}"
    subprocess.call(ffmpeg_resize_cmd, shell=True)

    # Create a file with a list of input videos
    input_list_file = "input_videos.txt"
    with open(input_list_file, "w") as f:
        f.write(f"file '{first_video_resized_path}'\n")
        f.write(f"file '{second_video_path}'\n")

    # Merge the videos
    output_file_name = os.path.splitext(os.path.basename(second_video_path))[
        0] + "_report.mp4"
    output_file_path = os.path.join(
        os.path.dirname(second_video_path), output_file_name)
    ffmpeg_merge_cmd = f"ffmpeg -f concat -safe 0 -i {input_list_file} -c copy {output_file_path}"
    subprocess.call(ffmpeg_merge_cmd, shell=True)

    # Remove the temporary files
    os.remove(first_video_resized_path)
    os.remove(input_list_file)

    return output_file_path


def create_video_content(working_folder: str = '/Users/lgg/Downloads'):
    # 存储 SRT 文件的路径
    srt_file_path = ''

    # 获取用户输入的视频 URL 或者视频 ID，下载最新视频，或者输入 v 使用 Download 文件夹的最新 .mp4 文件
    video_url = input("请输入 Youtube 视频 URL 或者 Youtube视频 ID 下载最新视频, 或者输入 v 使用 Download 文件夹的最新 .mp4 文件: \n")
    if not video_url: return

    if not video_url.lower() == 'v':
        try:
            # 下载视频，并获取 SRT 文件的路径
            srt_file_path = download_youtube_video(video_url, working_folder='/Users/lgg/Downloads')
            print(f"DEBUG: {video_url} 视频下载成功!")
        except Exception as e:
            print(f"ERROR: {video_url} 视频下载失败, 退出程序!\n\n{e}")
            return

    if video_url.lower() == 'v': 
        # 从 today_video_url_file 中 读出 video_url 
        today_video_url_file = os.path.join(working_folder, 'today_video_url.txt')
        with open(today_video_url_file, 'r') as f: video_url = f.read()

    # 获取最新的 .mp4 文件的路径
    filepath = get_latest_file_in_folder(working_folder, '.mp4')
    if not filepath: 
        print(f"ERROR: {working_folder} 文件夹中找不到 .mp4 文件, 退出程序!")
        return

    if not srt_file_path:
        if debug: print(f"DEBUG: whisper 将会为视频 {filepath.split('/')[-1]} 转录英文脚本...")

        # 从视频中提取音频，并转换为文本
        audio_path = extract_audio(filepath, extension='.mp3')
        srt_text = from_voice_to_text(audio_path)
        if not srt_text: 
            print(f"ERROR: {audio_path} 视频英文脚本转录失败!")
            return

        srt_file_path = audio_path[:-4] + ".srt"
        with open(srt_file_path, 'w') as f: f.write(srt_text)
        if debug: print(f"DEBUG: 脚本转录成功并保存为: {srt_file_path} ")

    if not os.path.isfile(srt_file_path):
        print(f"ERROR: {srt_file_path} 找不到视频脚本文件, 退出程序!")
        return

    # 如果文件存在，则开始处理视频
    if os.path.isfile(filepath):
        print(f"DEBUG: 成功找到最新视频文件, 开始处理视频...")

        # 重命名文件为 'today_video'，并返回文件路径列表
        output_video = ''
        target_filename = 'today_video'
        filepath_list = rename_target_file(filepath, target_filename)

        # 循环处理每个文件路径
        for filepath in filepath_list:
            if '.mp4' not in filepath: continue

            # 处理视频
            if debug: print(f"DEBUG: 开始处理 MP4 视频 {filepath}...")
            output_video = process_video(filepath, video_url)

        if output_video:
            if debug: print(f"DEBUG: 成功合成视频 {output_video}, 现在整理文件夹...")
            # 创建并获取最新的文件夹路径
            dirname, filename = os.path.split(srt_file_path)
            folder_name = filename.replace(' ', '_')
            latest_folder = os.path.join(dirname, folder_name[:-4])
            if not os.path.isdir(latest_folder): os.mkdir(latest_folder)

            # 将所有包含 'today_video' 的文件移动到最新的文件夹中
            for file in os.listdir(working_folder):
                if target_filename in file:
                    src_path = os.path.join(working_folder, file)
                    dst_path = os.path.join(latest_folder, file)
                    os.rename(src_path, dst_path)
            if debug: print(f"DEBUG: 视频等相关文件已经成功移到最新的文件夹中 {latest_folder}")

            # 进入 latest_folder 将 MP4 文件更名为与文件夹同名
            for file in os.listdir(latest_folder):
                if '.mp4' in file:
                    src_path = os.path.join(latest_folder, file)
                    dst_path = os.path.join(latest_folder, folder_name[:-4] + '.mp4')
                    os.rename(src_path, dst_path)
            if debug: print(f"DEBUG: 视频文件已经成功更名为 {folder_name[:-4]}.mp4")

            send_message(text=f'中文视频创建成功 \n\n{latest_folder}', chat_id=BOTOWNER_CHAT_ID)

        else: print(f"ERROR: {output_video} 创建失败, 退出程序!")
    return


if __name__ == "__main__":
    print(f"DEBUG: create_video.py started")

    try: create_video_content(working_folder='/Users/lgg/Downloads')
    except Exception as e: print(f"ERROR: {e}")

    # process_video('/Users/lgg/Downloads/today_video.mp4', 'https://www.youtube.com/watch?v=zizonToFXDs')