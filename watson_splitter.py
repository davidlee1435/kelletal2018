import json
import sys
import re
import os
from watson_developer_cloud import SpeechToTextV1
from pydub import AudioSegment

IBM_USERNAME = "kishansheth98@gmail.com"
IBM_PASSWORD = "IBMSheth123!"
API_KEY = "YaCluIB-3eK6u498HsPtssjgCSoD1IsW-Wjrw8GHpjq-"
URL = "https://stream.watsonplatform.net/speech-to-text/api"

if len(sys.argv) != 2:
    print("Provide audio file as first argument.")
    exit()

language = sys.argv[1]
file_location = "../recordings/" + language + ".mp3"

stt = SpeechToTextV1(iam_apikey=API_KEY, url=URL)
audio_file = open(file_location, "rb")

# for pydub splitting
BUFFER = 0 # in ms
audio_object = AudioSegment.from_file(file_location, format="mp3")
transcript_words = ['please', 'call', 'stella', 'ask', 'her', 'to', 'bring', 'these', 'things', 'with', 'her', 'from', 'the', 'store', 'six', 'spoons', 'of', 'fresh', 'snow', 'peas', 'five', 'thick', 'slabs', 'of', 'blue', 'cheese', 'and', 'maybe', 'a', 'snack', 'for', 'her', 'brother', 'bob', 'we', 'also', 'need', 'a', 'small', 'plastic', 'snake', 'and', 'a', 'big', 'toy', 'frog', 'for', 'the', 'kids', 'she', 'can', 'scoop', 'these', 'things', 'into', 'three', 'red', 'bags', 'and', 'we', 'will', 'go', 'meet', 'her', 'wednesday', 'at', 'the', 'train', 'station']

# mkdir if doesn't exist
if not os.path.exists("../splitAudio/" + language + "/"):
    os.mkdir("../splitAudio/" + language + "/")


# using Watson STT result
result = stt.recognize(audio_file, content_type="audio/mp3", continuous=True, timestamps=True, max_alternatives=1)
result_string = str(result)

# using dummy result
# with open('dummy_result.txt', 'r') as myfile:
#     result_string=myfile.read() #.replace('\n', '')

result_json = json.loads(result_string)
word_positions = result_json['result']['results'][0]['alternatives'][0]['timestamps']

print(result_json)
print(type(word_positions))
print(transcript_words)

for i, word_position in enumerate(word_positions):
    word = word_position[0]
    start = word_position[1] * 1000
    end = word_position[2] * 1000

    # buffer timestamps
    if word == transcript_words[0]:
        end = end + BUFFER
    elif word == transcript_words[len(transcript_words)-1]:
        start = start - BUFFER
    else:
        start = start - BUFFER
        end = end + BUFFER

    # export word chunks
    if word.lower() in transcript_words:
        word_chunk = audio_object[start:end]
        out_file = "../splitAudio/" + language + "/" + word + ".wav"
        word_chunk.export(out_file, format="wav")




### TOOLS ###

# extract words from speech_transcript
transcript_words = re.compile('\w+').findall("Please call Stella.  Ask her to bring these things with her from the store:  Six spoons of fresh snow peas, five thick slabs of blue cheese, and maybe a snack for her brother Bob.  We also need a small plastic snake and a big toy frog for the kids.  She can scoop these things into three red bags, and we will go meet her Wednesday at the train station.")

for i, word in enumerate(transcript_words):
    transcript_words[i] = word.lower()