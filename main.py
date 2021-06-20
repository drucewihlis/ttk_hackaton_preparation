import os
import pickle
import numpy as np
from scipy.io import wavfile
from drop_wav import get_audio_transcription
from drop_wav import get_diff_time
from SpeakerRecognizer import Speaker_Recognizing
import Norm_word as nw
from semantic import get_tone_estimate
#
# original_file = '11.05 38.wav'
#
# sample_rate, data = wavfile.read(original_file)
# get_audio_transcription(original_file)
# benefit_in_time = get_diff_time(original_file, "audio-chunks_full" + '/chunk_full.wav')
# print('Запись стала короче на  ', benefit_in_time, '%')
#
# out = Speaker_Recognizing()
#
# op_path = 'operator/'
# cl_path = 'client/'
#
# for i, file in enumerate(out['operator']):
#     os.rename('audio-chunks/' + file, op_path + file)
#
# for i, file in enumerate(out['client']):
#     os.rename('audio-chunks/' + file, cl_path + file)

text = []
text_rl_op = []
text_rl_cl = []

# text = nw.from_audio_to_text(nw.ch_file_short(out['operator']), nw.ch_file_short(out['client']), op_path, cl_path)

with open("Bad_Operator.txt") as f:
    text.append(f.read().lower())
with open('Bad_Operator.txt', 'r') as fp:
    for line in fp:
        text_rl_op.append(line.rstrip('\n'))
with open("Client.txt") as f:
    text.append(f.read().lower())

with open("Client.txt", 'r') as f:
    for line in f:
        text_rl_cl.append(line.rstrip('\n'))


print(get_tone_estimate(text_rl_op))

all_words = nw.words_from_data()
operator_result = nw.check_word_in_text_for_operator(all_words[0], text[0], all_words[1])
client_result = nw.check_word_in_text_for_man(all_words[0], text[1])

print(operator_result)
