import numpy as np

from joblib import load
import librosa.display
import os

from tensorflow.keras import *

import warnings
warnings.filterwarnings('ignore')

MODEL_PATH = 'ClassificationModel/model.h5'
SCALER_PATH = 'ClassificationModel/standard_scaler.bin'
ENCORED_PATH = 'ClassificationModel/label_encoder.bin'


class ClassificationModel:

    def __init__(self):
        self.model = models.load_model(MODEL_PATH)
        self.scaler = load(SCALER_PATH)
        self.encoder = load(ENCORED_PATH)

    def predictGenre(self, fileName: str) -> str:
        if not os.path.isfile(fileName):
            return None

        features = self.__extractFeatures(fileName)

        X = self.scaler.transform(np.array(features, dtype=float).reshape(-1, len(features)))

        predictions = self.model.predict_classes(X)
        labels = self.encoder.inverse_transform(predictions)

        if labels is None or len(labels) <= 0:
            return None

        return labels[0]

    def __extractFeatures(self, filename):
        y, sr = librosa.load(filename, mono=True, duration=30)
        chromaStft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        features = [np.mean(chromaStft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff),
                   np.mean(zcr)]
        for e in mfcc:
            features.append(np.mean(e))

        return features
