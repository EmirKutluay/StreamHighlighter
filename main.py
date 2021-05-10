import librosa
from pydub import AudioSegment
from scipy.io import wavfile
import moviepy.editor as mp
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips

video_file = "afidyo.mkv"
audio_file = "audio.aac"
folder_type = ".wav"

command = "ffmpeg -i " + video_file + " -map 0:v -c copy new_" + video_file + " -map 0:a:0 -c copy desktop_" + audio_file + " -map 0:a:1 -c copy mic_" + audio_file + " -map 0:a:2 -c copy noti_" + audio_file
subprocess.call(command, shell=True)

test, sr = librosa.load("mic_" + audio_file)

selected_times = librosa.effects.split(test, top_db=25)

sample_duration = 1 / sr
sample_num_each_milisecond = 0.001/sample_duration

i = 0
for x in selected_times:
    start = x[0] / sample_num_each_milisecond - 100
    end = x[1] / sample_num_each_milisecond + 100
    types = ["mic_", "desktop_", "noti_"]
    for t in types:
        audio = AudioSegment.from_file(t + audio_file)
        extract = audio[start:end]
        export_loc = t + str(i) + folder_type
        extract.export(export_loc, format="wav")
    ffmpeg_extract_subclip("new_" + video_file, start/1000, end/1000, targetname="new_" + str(i) + ".mp4")
    i += 1

time.sleep(1)

video_list = []

for t in range(len(selected_times)):
    desktop = AudioSegment.from_file("desktop_" + str(t) + ".wav", format="wav")
    mic = AudioSegment.from_file("mic_" + str(t) + ".wav", format="wav")
    noti = AudioSegment.from_file("noti_" + str(t) + ".wav", format="wav")
    combined = desktop + mic + noti
    combined.export("combined_" + str(t) + ".mp3", format="mp3")
    time.sleep(1)
    cmd = "ffmpeg -i new_" + str(t) + ".mp4 -i combined_" + str(t) + ".mp3 -c copy -map 0:v:0 -map 1:a:0 output_" + str(t) + ".mp4"
    subprocess.call(cmd, shell=True)
    time.sleep(1)
    video = VideoFileClip("output_" + str(t) + ".mp4")
    video_list.append(video)

final_video = concatenate_videoclips(video_list)
final_video.write_videofile("final_output.mp4")