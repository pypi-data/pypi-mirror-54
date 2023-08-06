import os
import re
from datetime import datetime
import numpy as np
import cv2


def getDepthVideo(path, silhouette_model, depth_height, depth_width):

    X = None
    files = []
    frameNumber = []
    timeStamps = []
    width, height = 160, 120

    for fileName in os.listdir(path):
        if re.match('.*.bin', fileName):
            files.append(fileName)
            frameNumber.append(int(fileName.split("__")[1]))
    files = [x for y, x in sorted(zip(frameNumber, files))]

    for i in range(0, len(files), 5):
        fileName = files[i]
        datetime_object = datetime.strptime(fileName.split(
            "__")[2].split("depth")[0], '%Y-%m-%d-%H-%M-%S-%f')
        timeStamps.append(datetime_object)
        frame = np.fromfile(
            path+fileName, dtype='uint16').reshape((depth_height, depth_width))

        frame = cv2.resize(frame, (320, 240)).reshape((1, 240, 320, 1))
        frame = frame.astype(np.float64)/np.amax(frame)
        # Model gives the silhoutte
        sil = silhouette_model.predict(frame).reshape((240, 320))
        frame = frame.reshape((240, 320))
        # connected component to remove unwanted parts
        fr = (sil > 0.5) * frame
        fr = (fr*255).astype(np.uint8)
        components = cv2.connectedComponents(fr)
        unique, counts = np.unique(components[1], return_counts=True)
        if len(unique) > 1:
            secondHighest = np.where(
                counts == np.partition(counts, -2)[-2])[0][0]
            sil = (components[1] == secondHighest)
        elif len(unique) == 1:
            sil = (components[1] == 0)

        frame = cv2.resize(np.multiply(frame, sil),
                           (width, height)).reshape((1, height, width))
        frame = frame/np.amax(frame)

        if X is None:
            X = frame
        else:
            X = np.concatenate((X, frame), axis=0)
    return X, timeStamps
