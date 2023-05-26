import csv
import os
import librosa
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd

#frame 2048 mẫu, bước nhảy 512 mẫu
# người trưởng thành có năng lượng cao hơn
def extractRMS(y):
    rms = librosa.feature.rms(y=y)
    return np.sum(rms[0]) / np.size(rms[0])
# trẻ em có giọng cao hơn nữ cao hơn nam
def extractPitch(y):
    spectrogram = librosa.feature.melspectrogram(y=y)
    return np.sum(spectrogram[0]) / np.size(spectrogram[0])
#trẻ em có khoảng lặng lớn hơn
def extractSilent_ratio(y):
    silent_ratio = 1.0 - np.count_nonzero(y) / float(len(y))
    return silent_ratio
# người trưởng thành có dải tần số rộng hơn
def extractBandwidth(y):
    spectral_banwidth = librosa.feature.spectral_bandwidth(y=y)
    return np.sum(spectral_banwidth[0]) / np.size(spectral_banwidth[0])
# tần số trung bình người trưởng thành cao hơn
def extractSpectralCentroid(y):
    spetral_centroid = librosa.feature.spectral_centroid(y=y)
    return np.sum(spetral_centroid[0]) / np.size(spetral_centroid[0])


def extractTrainData():
    with open('C:/Users/DELL/Desktop/HeCSDL_DPT-main/app/data/data.csv', 'a', newline="") as file:
            csvwriter = csv.writer(file)
            main_dir = "C:/Users/DELL/Desktop/HeCSDL_DPT-main/app/data"
            Id = -2
            # Loop through all the subfolders in the main directory
            for sub_dir in os.listdir(main_dir):
                # Construct the path to the subfolder
                sub_dir_path = os.path.join(main_dir, sub_dir)
                Id +=1
                # If the subfolder is a directory
                if os.path.isdir(sub_dir_path):
                    # Loop through all the .wav files in the subfolder
                    for file_name in os.listdir(sub_dir_path):
                        if file_name.endswith('.wav'):
                            # Construct the path to the audio file
                            file_path = os.path.join(sub_dir_path, file_name)
                            # print(file_name)
                            # Load the audio file using librosa
                            y, sr = librosa.load(file_path, sr=None)
                            data = []
                            data.append(extractRMS(y))
                            data.append(extractPitch(y))
                            data.append(extractSilent_ratio(y))
                            data.append(extractBandwidth(y))
                            data.append(extractSpectralCentroid(y))
                            if(Id==3):
                                Id=0
                            data.append(Id)
                            csvwriter.writerow(data)
                            print(file_name + " " + str(Id))




def predictNewData(newFile):
    data = []
    print('dang chay')
    y, sr = librosa.load(newFile)
    data.append(extractRMS(y))
    data.append(extractPitch(y))
    data.append(extractSilent_ratio(y))
    data.append(extractBandwidth(y))
    data.append(extractSpectralCentroid(y))
    print("data----------------------------------------------------------------------------------------------------------")
    print(data)
    max = -2
    label = 0
    with open("C:/Users/DELL/Desktop/HeCSDL_DPT-main/app/data/data.csv", 'r') as file:
        heading = next(file)
        csvReader = csv.reader(file)
        for row in csvReader:
            row = list(map(float, row))
            dataTrain = []
            for item in range(0, 5):
                dataTrain.append(row[item])
                # print(row[item])

            cosine_distance = dot(data, dataTrain) / (norm(data) * norm(dataTrain))
            # print(str(row[4]) + ',' + str(cosine_distance))
            if max < cosine_distance:
                # print(str(row[4]) + ',' + str(cosine_distance))
                print("train---------------------")
                print(dataTrain)
                print(cosine_distance)
                max = cosine_distance
                label = row[5]
    return [max, label]


def getNameFromLabel(label):
    label = int(label)
    with open("C:/Users/DELL/Desktop/HeCSDL_DPT-main/app/data/label.csv", 'r', encoding="utf8") as file:
        heading = next(file)
        csvReader = csv.reader(file)
        for row in csvReader:
            id = int(row[0])
            name = row[1]
            if id == int(label):
                return name
