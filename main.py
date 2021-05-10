import librosa
from pydub import AudioSegment

test_file = r"C:\Users\memir\Desktop\testaudio.wav"
folder_loc = r"C:\Users\memir\Desktop\testfolder\\"
folder_type = ".wav"

test, sr = librosa.load(test_file)

new = librosa.effects.split(test, top_db=45)

sample_duration = 1 / sr
sample_num_each_milisecond = 0.001/sample_duration

i = 0
for x in new:
    start = x[0] / sample_num_each_milisecond - 100
    end = x[1] / sample_num_each_milisecond + 100
    audio = AudioSegment.from_wav(r"C:\Users\memir\Desktop\testaudio.wav")
    extract = audio[start:end]
    export_loc = folder_loc + str(i) + folder_type
    print(export_loc)
    extract.export(export_loc, format="wav")
    i += 1
