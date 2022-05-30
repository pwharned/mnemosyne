import json
import io
import os
from src.db.database import DatabaseManager
from src.word_manager import WordManager
import base64
from pydub import AudioSegment
import librosa
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import numpy as np
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout, Flatten, Conv1D, Input, MaxPooling1D
from keras.models import Model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
from keras.models import load_model
from src.word import Word

### Load data from sqlite database, train a CNN to predict the label

path = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(path, "best_model.hdf5")
LABELS =os.path.join(path, "indexed_labels.json")
print(MODEL)

class Data:
    def __init__(self, language):
        self.database = DatabaseManager()
        self.language = language
        self.data = self.database.get_words(language)
        self.wav  = self.get_waves()

    def load_audio(self,audio_content):
        by = io.BytesIO(audio_content)
        return AudioSegment.from_file(by, format="mp3")

    def toWav(self,audio):
        out = io.BytesIO()
        return audio.export(out, format="wav")

    def get_labels(self):
        labels = [x[0] for x in self.data]
        return set(labels)


    def get_waves(self):
        return [ (x[0], self.toWav(self.load_audio(base64.b64decode(x[5].encode())))) for x in self.data]

    def process_wav(self):
        all_wave = []
        all_label = []
        for label in self.get_labels():
            waves = [x[1] for x in self.wav if x[0]==label]
            for wav in waves:
                print(wav)
                samples, sample_rate = librosa.load(wav, sr=8000 * 2)
                if len(samples) >= 8000:
                    samples = librosa.resample(samples, len(samples), 8000 * 2)
                    all_wave.append(samples)
                    all_label.append(label)
        return all_wave, all_label

    def write_labels(self):
        with open(LABELS, "w") as file:
            file.write(json.dumps(list(set(self.labels))))
        return None

    def fit_labels(self, labels):
        self.labels = labels
        self.write_labels()
        le = LabelEncoder()
        y = le.fit_transform(labels*10)
        self.classes = list(le.classes_)
        y = np_utils.to_categorical(y, num_classes=len(labels))
        return y

    def fit_waves(self, waves):
        return np.array(waves * 10).reshape(-1, 8000 * 2, 1)

    def training_data(self):
        all_wave, all_label = self.process_wav()
        labels = self.fit_labels(all_label)
        all_wave = self.fit_waves(all_wave)

        return labels, all_wave


class STTClassifier:
    def __init__(self, data):
        self.y, self.all_wave = data.training_data()
        self.labels = data.labels
        print(len(self.y))

    def train(self):
        x_tr, x_val, y_tr, y_val = train_test_split(np.array(self.all_wave), np.array(self.y), stratify=self.y, test_size=0.2, random_state=777, shuffle=True)
        K.clear_session()

        inputs = Input(shape=(8000 * 2, 1))

        # First Conv1D layer
        conv = Conv1D(8, 13, padding='valid', activation='relu', strides=1)(inputs)
        conv = MaxPooling1D(3)(conv)
        conv = Dropout(0.3)(conv)

        # Second Conv1D layer
        conv = Conv1D(16, 11, padding='valid', activation='relu', strides=1)(conv)
        conv = MaxPooling1D(3)(conv)
        conv = Dropout(0.3)(conv)

        # Third Conv1D layer
        conv = Conv1D(32, 9, padding='valid', activation='relu', strides=1)(conv)
        conv = MaxPooling1D(3)(conv)
        conv = Dropout(0.3)(conv)

        # Fourth Conv1D layer
        conv = Conv1D(64, 7, padding='valid', activation='relu', strides=1)(conv)
        conv = MaxPooling1D(3)(conv)
        conv = Dropout(0.3)(conv)

        # Flatten layer
        conv = Flatten()(conv)

        # Dense Layer 1
        conv = Dense(256, activation='relu')(conv)
        conv = Dropout(0.3)(conv)

        # Dense Layer 2
        conv = Dense(128, activation='relu')(conv)
        conv = Dropout(0.3)(conv)

        outputs = Dense(len(self.labels), activation='softmax')(conv)

        model = Model(inputs, outputs)
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10, min_delta=0.0001)
        mc = ModelCheckpoint('best_model.hdf5', monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
        history = model.fit(x_tr, y_tr, epochs=100, callbacks=[es, mc], batch_size=32, validation_data=(x_val, y_val))

        return history

class ClassifierLoader:
    def __init__(self):
        self.model = load_model(MODEL)
        self.read_labels()

    def read_labels(self):
        with open(LABELS, "r") as file:
            self.classes = json.loads(file.read())
        return None

    def predict(self,audio):
        samples = librosa.resample(audio, len(audio), 8000 * 2)
        prob = self.model.predict(samples.reshape(1, 8000 * 2, 1))

        index = np.argmax(prob[0])
        return self.classes[index]


if __name__=="__main__":
    data = Data("vietnamese")
    #model = STTClassifier(data)
    #model.train()

    classifier = ClassifierLoader()

    database = DatabaseManager()
    word = Word("y ta", "vietnamese")
    word2 = Word("Ong", "vietnamese")


    audio = word.get_word_audio()[0]
    audio2 = word2.get_word_audio()[0]


    print(word.word)
    print(classifier.predict(audio[1]))

    print(word2.word)
    print(classifier.predict(audio2[1]))
