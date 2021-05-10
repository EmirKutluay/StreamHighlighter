import librosa
from pydub import AudioSegment
from scipy.io import wavfile
import moviepy.editor as mp

video_file = "fidyo.mp4"
audio_file = "audio.wav"
mic_file = "audio_mic.wav"
folder_type = ".wav"

video = mp.VideoFileClip(video_file)
video.audio.write_audiofile(audio_file)

fs, audio = wavfile.read(folder_loc)
wavfile.write(mic_file, fs, audio[:, 1])

test, sr = librosa.load(mic_file)

selected_times = librosa.effects.split(test, top_db=25)

sample_duration = 1 / sr
sample_num_each_milisecond = 0.001/sample_duration

i = 0
for x in selected_times:
    start = x[0] / sample_num_each_milisecond - 100
    end = x[1] / sample_num_each_milisecond + 100
    audio = AudioSegment.from_file(mic_file)
    extract = audio[start:end]
    export_loc = str(i) + folder_type
    print(export_loc)
    extract.export(export_loc, format="wav")
    i += 1
