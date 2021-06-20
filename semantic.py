# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 16:09:00 2021

@author: Mi
"""
# -*- coding: utf-8 -*-
# -*- coding: cp1251 -*-

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import matplotlib.pyplot as plt


def get_tone_estimate(text):
    windows = []
    window_size = 5
    for phrase in text:
        phrase = phrase.split()
        if len(phrase) > window_size:
            for i in range(len(phrase) - window_size + 1):
                windows.append(' '.join(phrase[i:i + window_size]))
            else:
                windows.append(' '.join(phrase))

    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(windows, k=5)
    x_positive = []
    x_negative = []
    x_neutral = []
    for message, sentiment in zip(windows, results):
        x_positive.append(sentiment['positive'])
        x_negative.append(sentiment['negative'])
        x_neutral.append(sentiment['neutral'] + sentiment['skip'] + sentiment['speech'])
        print(message, '->', sentiment)
    fig, ax = plt.subplots()
    ax.plot(x_positive, label='positive')
    ax.plot(x_negative, label='negative')
    ax.plot(x_neutral, label='neutral')
    ax.set_xlabel('Время разговора')
    ax.set_title('Динамика тональности разговора оператора с течением времени')
    plt.legend()
    plt.grid()
    plt.show()


def take_text_split(text):
    text = text.split('\n')
    return text
