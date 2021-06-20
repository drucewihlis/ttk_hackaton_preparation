import pickle

import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

recog = sr.Recognizer()


def get_text_from_audio(file):
    sample_audio = sr.AudioFile(file)
    with sample_audio as audio_file:
        audio = recog.record(audio_file)

    return recog.recognize_google(audio, language="ru", show_all=False).lower()


def get_audio_transcription(file_path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    global audio_chunk_full, chunk_min
    sound = AudioSegment.from_wav(file_path)
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=200,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 12,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=200,
                              )
    print(chunks)
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = []
    # process each chunk
    j = 0
    chunk_min = 1
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        try:
            whole_text.append(get_text_from_audio(chunk_filename))
            if j == 0:
                audio_chunk_full = audio_chunk
                chunk_min = str(i)
            else:
                audio_chunk_full += audio_chunk
            j += 1
        except:
            os.remove(chunk_filename)
    chunk_filename = os.path.join(folder_name + '_full', f"chunk_full.wav")
    audio_chunk_full.export(chunk_filename, format="wav")
    os.rename(folder_name + '/chunk' + chunk_min + '.wav', folder_name + '/chunk1.wav')
    pickle.dump(whole_text, open('pickles/' + file_path + '.pkl', 'wb'))


def get_diff_time(original_file, cut_signal):
    import wave
    import contextlib
    with contextlib.closing(wave.open(cut_signal, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration1 = frames / float(rate)
    with contextlib.closing(wave.open(original_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration2 = frames / float(rate)
    return (duration1 / duration2) * 100
