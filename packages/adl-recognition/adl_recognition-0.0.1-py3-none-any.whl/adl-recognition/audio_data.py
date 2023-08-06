import os
import re
from datetime import datetime
import numpy as np
import librosa
import noisereduce as nr


def getAudioPath(path):
    audioFiles = []
    for file in os.listdir(path):
        if re.match('.*.wav', file) and int(file.split("__")[1].split(".")[0]) > 1:
            audioFiles.append(path+file)
    return audioFiles


def getX_a(audio_file, sample_rate, audio_start, depth_start, depth_end):
    # load audio data
    initialDifference = (depth_start-audio_start).total_seconds()
    duration = (depth_end-depth_start).total_seconds()
    segmentStart = int(initialDifference*sample_rate)
    segmentEnd = int(min((initialDifference+duration)
                         * sample_rate, len(audio_file)-1))
    segment = audio_file[segmentStart:segmentEnd]
    stft = np.abs(librosa.stft(segment, n_fft=512,
                               hop_length=256, win_length=512))
    return np.mean(stft, axis=1)


def processAudioData(audio_file_path):
    audioFiles = getAudioPath(audio_file_path)

    raw_audio, sample_rate = librosa.load(audioFiles[0])
    datetime_audio = datetime.strptime(audioFiles[0].split(
        "__")[0].split("\\")[-1], '%Y-%m-%d-%H-%M-%S-%f')

    noisy_part = raw_audio[0:25000]
    nr_audio = nr.reduce_noise(
        audio_clip=raw_audio, noise_clip=noisy_part, verbose=False)
    return nr_audio, sample_rate, datetime_audio
