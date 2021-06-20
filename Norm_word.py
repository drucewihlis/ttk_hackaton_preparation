from difflib import SequenceMatcher
import numpy as np
import itertools
import pymorphy2
import docx2txt
import pandas as pd

import speech_recognition as sr
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence


def to_base_form(word, morph):
    p = morph.parse(word)[0]
    return p.normal_form


def get_format_string(row):
    morph = pymorphy2.MorphAnalyzer()
    row = row.split()
    words_base = [to_base_form(word, morph) for word in row]
    s = ""
    for i in words_base:
        s += i + " "
    return s


def words_from_data():
    row = docx2txt.process("bad_word.docx")
    s = ""
    for i in row:
        if i != ',' and i != '_':
            s += i

    row = s.lower()
    row = row.split()
    bad_words = {a: [-100, 1] for a in row}

    file_name = "Запрещенные_фразы.xlsx"
    d = pd.read_excel(file_name).to_numpy()
    # print(d)
    dict_not_good_word = bad_words
    for i in d:
        if i[1] == i[1]:
            if i[2] == i[2]:
                dict_not_good_word[i[1].lower()] = [i[2], 1]
            else:
                dict_not_good_word[i[1].lower()] = [-0.5, 1]

    file_name = "Речевые_модули.xlsx"
    d = pd.read_excel(file_name).to_numpy()
    phrase = []
    for i in d:
        if i[1] == i[1]:
            s = ""
            for n in i[1]:
                if n not in ",./?\|[]{}-_+=)(&*!@#$%^)":
                    s += n

            h = get_format_string(s)
            h = h.split()
            phrase.append(h)
            # dict_not_good_word[h] = [1, 1]
    return dict_not_good_word, phrase


def text_from_audio(file):
    recog = sr.Recognizer()
    sample_audio = sr.AudioFile(file)
    with sample_audio as audio_file:
        audio = recog.record(audio_file)

    return recog.recognize_google(audio, language="ru", show_all=False)


def phraza_check(str_mas):
    similarity = lambda x: np.mean([SequenceMatcher(None, a, b).ratio() for a, b in itertools.combinations(x, 2)])
    out = similarity(str_mas)
    return out


def listsum(numList):
    theSum = ""
    for i in numList:
        theSum += i + " "
    return theSum


def check_word_in_text_for_man(dict_word, text):
    text = get_format_string(text)
    text = text.split()
    l = len(text)
    j = 0
    rating = []
    jj = 0
    rating_part = []
    for i, n in enumerate(text):

        if i > l / 3 + l / 3:
            if len(rating_part) > 1:
                rating.append(rating_part)
            rating_part = []
            rating_phrase_part = []
            j = 2
        elif i > l / 3:
            if len(rating_part) > 1:
                rating.append(rating_part)
            rating_part = []
            rating_phrase_part = []
            j = 1
        if n in dict_word:
            # print(n)
            # print(dict_word[n])
            rating_part.append(dict_word[n])
            rating_part.append(n)

    rating.append(rating_part)
    return rating


def check_word_in_text_for_operator(dict_word, text, phrase):
    text = get_format_string(text)
    text = text.split()
    l = len(text)
    j = 0
    rating = []
    rating_phrase = []

    mas_phrase = []
    mas_ph_i = []
    for i, m in enumerate(phrase):
        mas_phrase.append(m[0])
        mas_ph_i.append(i)
        if len(m) > 1:
            mas_phrase.append(m[1])
            mas_ph_i.append(i)
        if len(m) > 2:
            mas_phrase.append(m[2])
            mas_ph_i.append(i)

    jj = 0
    rating_part = []
    rating_phrase_part = []
    for i, n in enumerate(text):

        if i > l / 3 + l / 3:
            if len(rating_part) > 1:
                rating.append(rating_part)
            if len(rating_phrase_part) > 1:
                rating_phrase.append(rating_phrase_part)
            rating_part = []
            rating_phrase_part = []
            j = 2
        elif i > l / 3:
            if len(rating_part) > 1:
                rating.append(rating_part)
            if len(rating_phrase_part) > 1:
                rating_phrase.append(rating_phrase_part)
            rating_part = []
            rating_phrase_part = []
            j = 1
        if n in dict_word:
            rating_part.append(dict_word[n])
            rating_part.append(n)
        if n in mas_phrase:
            yy = []
            for p, y in enumerate(mas_phrase):
                if y == n:
                    yy.append(mas_ph_i[p])
            ll = []
            ph = 0
            i_ph = 0
            for mm in yy:
                row = phrase[mm]
                row = listsum(row)
                str_new = ""
                for kk in range(i, i + len(phrase[mm])):
                    if kk > len(text) - 1:
                        break
                    str_new += text[kk] + " "
                ph_n = phraza_check([str_new, row])
                if ph_n >= ph:
                    i_ph = mm
                    ph = ph_n

            # print("NEXT")
            if ph > 0.75 and phrase[i_ph] not in rating_phrase_part:
                rating_phrase_part.append(ph)
                rating_phrase_part.append(phrase[i_ph])

    rating.append(rating_part)
    rating_phrase.append(rating_phrase_part)
    return rating, rating_phrase


def from_audio_to_text(operator, man, op_path, cl_path):
    text_operator = ""
    text_man = ""
    for n in operator:
        text_operator += text_from_audio(op_path + n) + " "
    for n in man:
        text_man += text_from_audio(cl_path + n) + " "

    return text_operator, text_man


def ch_file_short(mas):
    word = 'chunk'
    i_d = []
    for i, n in enumerate(mas):
        nomer = n[len(word):len(n) - 4]
        i_d.append(int(nomer))

    masiv_i = i_d.copy()
    masiv_out = []
    i_d.sort()
    for i in i_d:
        for j, m in enumerate(masiv_i):
            if i == m:
                masiv_out.append(mas[j])
                break
    return masiv_out
