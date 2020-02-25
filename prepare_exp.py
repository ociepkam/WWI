#!/usr/bin/env python
# -*- coding: utf8 -*

import random
import numpy as np
from psychopy import visual
import copy

stim = ['WYSOKA', 'UKRYTA', u'GŁĘBOKA', 'DALEKA']

last_text = None
last_text_2 = None


def prepare_trial(trial_type, win, text_height, words_dist, color='black'):
    global last_text, last_text_2
    text = None
    stim_distr = None

    if trial_type == 'congruent':
        possible_text = stim[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text)
        words = [text, text]

    elif trial_type == 'incongruent':
        possible_text = stim[:]
        if last_text is not None:
            for elem in last_text:
                if elem in possible_text:
                    possible_text.remove(elem)
        text = np.random.choice(possible_text, 2)
        words = [text[0], text[1]]

    else:
        raise Exception('Wrong trigger type')

    random.shuffle(words)
    print(trial_type, text)
    last_text = text if len(text) == 2 else [text]
    last_text_2 = stim_distr

    stim1 = visual.TextStim(win, color=color, text=words[0], height=text_height, pos=(0, words_dist / 2))
    stim2 = visual.TextStim(win, color=color, text=words[1], height=text_height, pos=(0, -words_dist / 2))
    print({'trial_type': trial_type, 'text': words, 'stim': [stim1, stim2]})
    return {'trial_type': trial_type, 'text': words, 'stim': [stim1, stim2]}


def prepare_part(trials_congruent, trials_incongruent, win, text_height, words_dist, color):
    trials = ['congruent'] * trials_congruent + \
             ['incongruent'] * trials_incongruent
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, text_height, words_dist, color) for trial_type in trials]


def prepare_exp(data, win, text_size):
    text_height = 1.5 * text_size
    training_trials = prepare_part(data['Training_trials_congruent'], data['Training_trials_incongruent'],
                                   win, text_height, data["words_dist"], data['words_color'])

    experiment_trials = prepare_part(data['Experiment_trials_congruent'], data['Experiment_trials_incongruent'],
                                     win, text_height, data["words_dist"], data['words_color'])

    return training_trials, experiment_trials
