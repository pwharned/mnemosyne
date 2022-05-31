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
from src.word import Word

import librosa
class Reviewer:
    def __init__(self, language):
        self.database = DatabaseManager()
        self.model = ClassifierLoader()
        self.language = language

    def record(self):
        print("start")
        mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
        print("end")
        sd.wait()
        time.sleep(2)
        sd.play(mydata, 16000)
        time.sleep(2)
        sf.write(filename, mydata, samplerate)
        return mydata

    def predict(self):
        self.record()
        samples, sample_rate = librosa.load(filename, sr=16000)
        return self.model.predict(samples)

    def get_words(self):
        words = [Word(x[0], language=self.language) for x in self.database.get_words(self.language)]
        return words

    def get_words_to_study(self):
        words = [Word(x[0], language=self.language) for x in self.database.get_words_to_study(self.language)]
        return words

    def increase_level(self, word):
        number_days = word.get_level()
        number_days  = 1 if number_days <= 0 else number_days
        statement = f"UPDATE WORDS SET LEVEL=LEVEL+1 , NEXT_STUDY = DATETIME(NEXT_STUDY, '+{number_days} DAYS') WHERE WORD = '{word.word}'"
        return self.database.execute(statement=statement)
    def decrease_level(self, word):
        number_days = word.get_level()
        level = 0 if number_days == 0 else 1
        statement = f"UPDATE WORDS SET LEVEL=LEVEL-{level} , NEXT_STUDY = DATETIME(NEXT_STUDY, '-{number_days} DAYS') WHERE WORD = '{word.word}'"
        return self.database.execute(statement=statement)







if __name__=="__main__":
    reviewer = Reviewer("vietnamese")
    words = reviewer.get_words_to_study()
    for x in words:
        x.play()
        translation = Word(x.get_translation(), "english")
        translation.play_api()
        time.sleep(2)
        prediction = reviewer.predict()
        if prediction == x.word:
            print("Succes! you guessed the word correctly")
            reviewer.increase_level(x)
        else:
            print("Try Again")
            reviewer.decrease_level(x)



