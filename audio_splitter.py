import os
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence

# MOST ACCURATE PARAMETERS
# min_silence_len=100
# silence_thresh=-30

if len(sys.argv) != 2:
    print("Provide audio file name as arg.")
    sys.exit()

language = sys.argv[1]

# split audio into chunks
sound_file = AudioSegment.from_file("./recordings/" + language + ".mp3", format="mp3")
audio_chunks = split_on_silence(sound_file, min_silence_len=100, silence_thresh=-30)

print("Number of chunks: ", len(audio_chunks))

# mkdir if doesn't exist
if not os.path.exists("./splitAudio/" + language + "/"):
    os.mkdir("./splitAudio/" + language + "/")

# export chunks
for i, chunk in enumerate(audio_chunks):
    out_file = "./splitAudio/" + language + "/chunk{0}.wav".format(i)
    print("exporting", out_file)
    chunk.export(out_file, format="wav")