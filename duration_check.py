import os
import torchaudio


def filter_audio_files(input_folder, output_folder, target_duration=10):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.wav'):
            file_path = os.path.join(input_folder, filename)
            audio, _ = torchaudio.load(file_path)
            duration = audio.size(1) / audio.size(0)  # Calculate duration in seconds

            if duration == target_duration:
                output_path = os.path.join(output_folder, filename)
                os.rename(file_path, output_path)
                print(f"Kept {filename} with duration {duration} seconds")
            else:
                os.remove(file_path)
                print(f"Deleted {filename} with duration {duration} seconds")


# Example usage
input_folder = "D:\PycharmProjects\Gans Project\music_data"
output_folder = "D:\PycharmProjects\Gans Project\music_cap_10"
filter_audio_files(input_folder, output_folder)
