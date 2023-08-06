import os
from sklearn.preprocessing import LabelEncoder
from audio_data import processAudioData
from depth_data import getDepthVideo
from model import getModel
from predict import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predictADL(audio_file_path, depth_file_path, sil_model_path=r"../models/2019_09_27_02_56_29_2", classifier_path=r"../models/15_07_14_acc_92", depth_skipping_frames=1, depth_win_size=15, hop_length=1, selectedActivities=['StandStill', 'Walking', 'SitStill', 'Sitting', 'PickingObject', 'Sleeping', 'StandUp', 'LyingDown', 'Falling', 'WakeUp']):
    nr_audio, sample_rate, datetime_audio = processAudioData(audio_file_path)

    sil_model = getModel(sil_model_path)
    classifier_model = getModel(classifier_path)

    video, timeStamps = getDepthVideo(depth_file_path, sil_model, 480, 640)

    lb = LabelEncoder()
    lb.fit_transform(selectedActivities)

    predictions = predict(classifier_model, video, timeStamps, nr_audio, sample_rate,
                          datetime_audio, selectedActivities, depth_skipping_frames, depth_win_size, hop_length)

    show(video, predictions, lb)
