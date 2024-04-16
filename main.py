import subprocess
import os
from pathlib import Path

from datasets import load_dataset, Audio

def download_video(video_id, output_filename):
    command = f"yt-dlp --quiet --no-warnings --format 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o '{output_filename}' https://www.youtube.com/watch?v={video_id}"
    subprocess.run(command, shell=True, check=True)


def extract_audio(input_video, output_audio, start_time, end_time):
    command = f"ffmpeg -y -i '{input_video}' -ss {start_time} -to {end_time} -vn -acodec pcm_s16le -ar 44100 -ac 2 '{output_audio}'"
    subprocess.run(command, shell=True, check=True)

def main(
    data_dir: str,
    limit: int = None,
):
    """
    Download the clips within the MusicCaps dataset from YouTube.

    Args:
        data_dir: Directory to save the clips to.
        limit: Limit the number of examples to download.
    """

    ds = load_dataset('google/MusicCaps', split='train')
    if limit is not None:
        print(f"Limiting to {limit} examples")
        ds = ds.select(range(limit))

    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True, parents=True)

    for example in ds:
        output_video = data_dir / f"{example['ytid']}.mp4"
        output_audio = data_dir / f"{example['ytid']}.wav"

        if not os.path.exists(output_audio):
            download_video(example['ytid'], output_video)
            extract_audio(output_video, output_audio, example['start_s'], example['end_s'])

        example['audio'] = str(output_audio)
        example['download_status'] = os.path.exists(output_audio)

    return ds

if __name__ == '__main__':
    ds = main('./music_data', limit=100)
