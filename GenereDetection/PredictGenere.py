
import pandas as pd
import numpy as np

from joblib import load
import librosa.display

from tensorflow.keras import *

import warnings
warnings.filterwarnings('ignore')


if __name__ == '__main__':

    model = models.load_model('model.h5')
    scaler = load('standard_scaler.bin')
    encoder = load('label_encoder.bin')

    songName = 'test.mp3'
    y, sr = librosa.load(songName, mono=True, duration=30)
    chromaStft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    features = [np.mean(chromaStft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    for e in mfcc:
        features.append(np.mean(e))

    X = scaler.transform(np.array(features, dtype=float).reshape(-1, len(features)))

    predictions = model.predict_classes(X)
    labels = encoder.inverse_transform(predictions)
    print(labels)