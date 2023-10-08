import os
import ast
import numpy as np
import copy
import calendar
import time
import argparse
import json
import logging
import matplotlib.pyplot as plt
import moviepy.editor
import cv2
import librosa
from util import *
from envload import *
import datetime
import subprocess

# audio_path = RGB_BASELINE_FOLDER_PATH + PNAME + '-BL-audio.MP3'
# audio_path = RGB_DRIVER1_FOLDER_PATH + PNAME + '-D1-audio.MP3'
# audio_path = RGB_DRIVER2_FOLDER_PATH + PNAME + '-D2-audio.MP3'
# audio_path = RGB_DRIVER3_FOLDER_PATH + PNAME + '-D3-audio.MP3'
# audio_path = RGB_PASSENGER1_FOLDER_PATH + PNAME + '-P1-audio.MP3'
audio_path = RGB_PASSENGER2_FOLDER_PATH + PNAME + '-P2-audio.MP3'

def showFigureOnset(y, times, o_env):
    D = np.abs(librosa.stft(y))
    fig, ax = plt.subplots(nrows=2, sharex=True)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                            x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set(title='Power spectrogram')
    ax[0].label_outer()
    ax[1].plot(times, o_env, label='Onset strength')
    # ax[1].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
    #            linestyle='--', label='Onsets')
    ax[1].legend()
    fig.show()
    pass

def getMaxOnsetInAudio(audio_path):
    max_len = 4
    y, sr = librosa.load(audio_path)
    librosa.onset.onset_detect(y=y, sr=sr, units='time')

    o_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(o_env, sr=sr)
    showFigureOnset(y, times, o_env)
    # onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
    # max_onset_frame = np.argmax(o_env)
    max_onset_frame = np.argsort(o_env)[-max_len:]
    max_onset = o_env[max_onset_frame]
    max_onset_time = times[max_onset_frame]
    len_frame_of_time = len(times)
    return max_onset, max_onset_frame, max_onset_time, len_frame_of_time

max_onset, max_onset_frame, max_onset_time, len_frame_of_time = getMaxOnsetInAudio(audio_path)
print(max_onset, max_onset_frame, max_onset_time, len_frame_of_time)
pass  