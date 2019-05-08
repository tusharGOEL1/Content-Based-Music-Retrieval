
import librosa
from pysndfx import AudioEffectsChain
import numpy as np
import math
import python_speech_features
import scipy as sp
import os
from scipy import signal

'''------------------------------------
FILE READER:
    receives filename,
    returns audio time series (y) and sampling rate of y (sr)
------------------------------------'''


BASE_DIR1 = os.path.abspath(os.path.dirname(__file__))
def read_file(file_name):


    # generating audio time series and a sampling rate (int)
    y, sr = librosa.load(file_name)

    return y, sr


def reduce_noise_mfcc_up(y, sr):

    hop_length = 512

    ## mfcc
    mfcc = python_speech_features.base.mfcc(y)
    mfcc = python_speech_features.base.logfbank(mfcc)
    mfcc = python_speech_features.base.lifter(mfcc)

    sum_of_squares = []
    index = -1
    # for r in mfcc:
    #     sum_of_squares.append(0)
    #     index = index + 1
    #     for n in r:
    #         sum_of_squares[index] = sum_of_squares[index] + n**2
    sum_of_squares = np.sum(np.square(mfcc), axis=1)

    strongest_frame = np.argmax(sum_of_squares)
    hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

    max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().lowshelf(frequency=min_hz*(-1), gain=12.0, slope=0.5)#.highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.5)#.limiter(gain=8.0)
    y_speach_boosted = speech_booster(y)

    return (y_speach_boosted)


'''------------------------------------
SILENCE TRIMMER:
    receives an audio matrix,
    returns an audio matrix with less silence and the amout of time that was trimmed
------------------------------------'''
def trim_silence(y):
    y_trimmed, index = librosa.effects.trim(y, top_db=20, frame_length=2, hop_length=500)
    trimmed_length = librosa.get_duration(y) - librosa.get_duration(y_trimmed)

    return y_trimmed, trimmed_length


'''------------------------------------
AUDIO ENHANCER:
    receives an audio matrix,
    returns the same matrix after audio manipulation
------------------------------------'''
def enhance(y):
    apply_audio_effects = AudioEffectsChain().lowshelf(gain=10.0, frequency=260, slope=0.1).reverb(reverberance=25, hf_damping=5, room_scale=5, stereo_depth=50, pre_delay=20, wet_gain=0, wet_only=False)#.normalize()
    y_enhanced = apply_audio_effects(y)

    return y_enhanced

'''------------------------------------
OUTPUT GENERATOR:
    receives a destination path, file name, audio matrix, and sample rate,
    generates a wav file based on input
------------------------------------'''
def output_file(destination ,filename, y, sr, ext=""):
    destination = os.path.join(destination, filename[:-4] + ext + '.wav')
    librosa.output.write_wav(destination, y, sr)


'''------------------------------------
LOGIC:
    [1] load file
    [2] reduce noise
    [3] trim silence
    [4] output file
sample files:
    01_counting.m4a
    02_wind_and_cars.m4a
    03_truck.m4a
    04_voices.m4a
    05_ambeint.m4a
    06_office.m4a
------------------------------------'''
#samples = ['01_counting.m4a','02_wind_and_cars.m4a','03_truck.m4a','04_voices.m4a','05_ambeint.m4a','06_office.m4a']

def noisered(filename,flag) :

    f = os.path.basename(filename)

    try:
        y, sr = read_file(filename)
    except:
        return None
    if os.path.exists(os.path.join(BASE_DIR1, filename.replace('.mp3', '.wav'))):
        return os.path.join(BASE_DIR1,"01_samples_trimmed_noise_reduced", f + '.wav')

    y_reduced_mfcc_up = reduce_noise_mfcc_up(y, sr)
    y_reduced_mfcc_up, time_trimmed = trim_silence(y_reduced_mfcc_up)

    if flag == 0 :
        path = os.path.join(BASE_DIR1,"01_samples_trimmed_noise_reduced")
        output_file(path ,f, y_reduced_mfcc_up, sr, '')

    else :
        path = os.path.join(BASE_DIR1,"processed_songs")

        output_file(path ,f, y_reduced_mfcc_up, sr, '')

    f=os.path.splitext(f)[0]

    return os.path.join(BASE_DIR1,"01_samples_trimmed_noise_reduced", f + '.wav')