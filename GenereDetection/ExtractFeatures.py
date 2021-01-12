import librosa
import numpy as np
import os
import librosa.display
import matplotlib.pyplot as plt
import csv

import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    headers = ['filename', 'chroma_stft', 'rmse', 'spectral_centroid', 'spectral_bandwidth', 'rolloff', 'zero_crossing_rate']
    for i in range(1, 21):
        headers.append(f'mfcc{i}')
    headers.append('label')

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        for genre in genres:
            for filename in os.listdir(f'./dataset/{genre}'):
                print(f'Processing file {filename}')

                songName = f'./dataset/{genre}/{filename}'
                y, sr = librosa.load(songName, mono=True, duration=30)
                chromaStft = librosa.feature.chroma_stft(y=y, sr=sr)
                rmse = librosa.feature.rms(y=y)
                spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                zcr = librosa.feature.zero_crossing_rate(y)
                mfcc = librosa.feature.mfcc(y=y, sr=sr)
                fatures = [filename, np.mean(chromaStft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
                for e in mfcc:
                    fatures.append(np.mean(e))
                fatures.append(genre)

                writer.writerow(fatures)
                file.flush()
