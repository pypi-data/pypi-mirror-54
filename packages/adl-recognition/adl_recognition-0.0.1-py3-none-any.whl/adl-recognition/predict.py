from audio_data import getX_a
import numpy as np
import cv2


def predict(model, video, timeStamps, nr_audio, sample_rate, datetime_audio, activities, depth_skipping_frames, depth_win_size, hop_length):
    width, height = 160, 120
    startFrameNumber = 0
    numOfFrames = video.shape[0]
    numOfActivities = len(activities)
    predictions = np.zeros((numOfFrames, numOfActivities))
    for i in range(0, numOfFrames - depth_win_size*depth_skipping_frames+depth_skipping_frames, hop_length):
        array = [j for j in range(
            i, i+depth_win_size*depth_skipping_frames, depth_skipping_frames)]
        clip = video[array]
        audio_features = getX_a(nr_audio, sample_rate, datetime_audio,
                                timeStamps[array[0]+startFrameNumber], timeStamps[array[-1]+startFrameNumber])
        res = model.predict([clip.reshape((1, clip.shape[0], height, width, 1)),
                             audio_features.reshape((1, audio_features.shape[0]))])
        k = 0
        midVal = (depth_win_size-1)/2
        for j in array:
            weight = (1/midVal)*(midVal-abs(k-midVal))
            predictions[j] += res.reshape((numOfActivities))*weight
            k += 1
    return predictions


def show(video, predictions, labelEncoder):
    i = 0
    previ = -1

    while True:
        if i == -1:
            i = len(predictions)
        if(i == len(predictions)):
            i = 0

        if i != previ:
            pred = predictions[i].copy()
            total = sum(pred)
            action = labelEncoder.inverse_transform([np.argmax(pred)])[0]
            confidence = "NaN"
            if(not total == 0):
                confidence = str(round(pred[np.argmax(pred)]/total, 2))

            pred[np.argmax(pred)] = 0

        img = cv2.resize((video[i]*255).astype(np.uint8), (960, 720))
        cv2.putText(img, action+" "+confidence, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (60000, 60000, 60000), lineType=cv2.LINE_AA)

        cv2.imshow("ADL predictions", img)
        k = cv2.waitKey(33)
        previ = i
        if(k == 13):
            i += 1
        elif (k == 46):
            i -= 1
        elif(k == 32):
            break
        if(i == len(predictions)):
            break

    cv2.destroyAllWindows()
