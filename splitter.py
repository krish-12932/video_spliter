import os
import subprocess
import math
import re
import imageio_ffmpeg

def get_ffmpeg_exe():
    """Returns the path to the ffmpeg executable from imageio-ffmpeg."""
    return imageio_ffmpeg.get_ffmpeg_exe()

def get_video_duration(filepath):
    """Gets the duration of the video in seconds using ffmpeg -i parsing."""
    ffmpeg_exe = get_ffmpeg_exe()
    try:
        # ffmpeg -i file will print info to stderr
        command = [ffmpeg_exe, '-i', filepath]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Parse Duration from stderr
        # Output format example: "  Duration: 00:00:10.54, start: 0.000000, bitrate: ..."
        output = result.stderr
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d+)", output)
        
        if match:
            hours = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        return None
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def split_video(filepath, clip_duration, output_folder):
    """
    Splits the video into clips of 'clip_duration' seconds.
    Returns a list of generated filenames.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    duration = get_video_duration(filepath)
    if not duration:
        raise ValueError("Could not determine video duration.")

    num_clips = math.ceil(duration / clip_duration)
    generated_files = []

    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    ffmpeg_exe = get_ffmpeg_exe()

    for i in range(num_clips):
        start_time = i * clip_duration
        output_filename = f"{name}_part{i+1}{ext}"
        output_path = os.path.join(output_folder, output_filename)
        
        # FFmpeg command to slice video
        command = [
            ffmpeg_exe, '-y',
            '-ss', str(start_time),
            '-t', str(clip_duration),
            '-i', filepath,
            '-c', 'copy',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            generated_files.append(output_filename)
        except subprocess.CalledProcessError as e:
            print(f"Error splitting part {i+1}: {e}")

    return generated_files
