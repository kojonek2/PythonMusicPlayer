import pandas as pd
import numpy as np

from joblib import dump

from tensorflow.keras import *

# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    data = data.drop(['filename'], axis=1)

    labels = data.iloc[:, -1]
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)  # change labels to numbers

    scaler = StandardScaler()
    X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype=float))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # take 20% as test data


    #Classification

    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(.2))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=100, batch_size=128)

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print('test_acc: ', test_acc)

    model.save('model.h5')
    dump(scaler, 'standard_scaler.bin', compress=True)
    dump(encoder, 'label_encoder.bin', compress=True)

