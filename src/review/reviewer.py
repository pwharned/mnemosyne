import sounddevice as sd
import soundfile as sf
import os
import time
from src.db.database import DatabaseManager
from src.model.model import ClassifierLoader
samplerate = 16000
duration = 2 # seconds
path = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(path, "file.wav")
from pydub.playback import play
from src.word import Word

import librosa
class Reviewer:
    def __init__(self, language):
        self.database = DatabaseManager()
        self.model = ClassifierLoader()
        self.language = language

    def record(self):
        print("start")
        mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=True)
        print("end")
        sd.wait()
        sd.wait()
        sf.write(filename, mydata, samplerate)
        return mydata

    def predict(self):
        self.record()
        samples, sample_rate = librosa.load(filename, sr=None)
        self.model.predict(samples)

    def get_words(self):
        words = [Word(x[0], language=self.language) for x in self.database.get_words(self.language)]
        return words






if __name__=="__main__":
    reviewer = Reviewer("vietnamese")
    words = reviewer.get_words()
    for x in words:
        x.play()
        time.sleep(2)


