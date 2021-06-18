import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence




recog=sr.Recognizer()
def r(file):
    sample_audio=sr.AudioFile(file)
    with sample_audio as audio_file:
        #recog.adjust_for_ambient_noise(audio_file)
        audio = recog.record(audio_file)

    print("You said: ", recog.recognize_google(audio, language="ru", show_all=False))








# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 200,
        # adjust this per requirement
        silence_thresh = sound.dBFS-12,
        # keep the silence for 1 second, adjustable as well
        keep_silence=200,
    )
    print(chunks)
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        print(chunk_filename)
        try:
            r(chunk_filename)
            #str = recog.recognize_google(audio, language="ru", show_all=False)
            #print(str)
        except:
            os.remove(chunk_filename)
            print("No", i)


    # return the text for all chunks detected
    return whole_text


print(get_large_audio_transcription("1.wav"))
