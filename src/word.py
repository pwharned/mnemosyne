base_url = "https://howtopronounce.com"
import os
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from pydub import AudioSegment
import base64
from src.db.database import DatabaseManager
import io
import librosa
import sounddevice as sd


def toWav(audio):
    out = BytesIO()
    return audio.export(out, format="wav")

class Word:
    def __init__(self, word, language):
        self.word = word
        self.language = language
        self.database = DatabaseManager()
        self.level = None

    def get_page(self):
        word = self.word.rstrip(" ").lstrip(" ").replace(" ", "-")
        url = os.path.join(base_url, self.language, word)
        print(url)
        return requests.get(url).content

    def get_audio_url(self, page):
        soup = BeautifulSoup(page, "html.parser")
        meta = soup.find_all('meta', {"property": "og:audio"})
        if len(meta) > 0:
            return meta[0]["content"]
        else:
            return None

    def get_translation(self):
        body = {"q": self.word, "source": "vi", "target": "en", "format": "text"}
        res = requests.post("https://libretranslate.de/translate", params = body)
        if res.status_code ==200:
            return res.json().get("translatedText")
        else:
            print(res.content)
            return None


    def get_audio_urls(self,page):
        soup = BeautifulSoup(page, "html.parser")
        meta = soup.find_all('meta', {"property": "og:audio"})
        if len(meta) > 0:
            return [x["content"] for x in meta]
        else:
            return None

    def download_audio(self,url):
        response = requests.get(url)
        if response.status_code > 300:
            print(response.content)
            return None
        else:
            return response.content

    def load_audio(self, audio_content):
        by = BytesIO(audio_content)
        return AudioSegment.from_file(by, format="mp3")

    def sample(self, audio):
        samples, sample_rate = librosa.load(toWav(audio), sr=16000)
        return samples

    def get_audio(self):
        page = self.get_page()
        audio_urls = self.get_audio_urls(page)
        audio = [self.download_audio(x) for x in audio_urls]
        return audio
    def toWav(self,audio):
        out = io.BytesIO()
        return audio.export(out, format="wav")

    def get_word_audio(self):
        # gets the audio as a b64 encoded string from the database for prediction
        return [(x[0], librosa.load(self.toWav(self.load_audio(base64.b64decode(x[1].encode()))),sr=16000 )[0] ) for x in self.database.get_word_audio(self.word) ]

    def play(self):
        self.audio = self.get_word_audio()[0][1]
        sd.play(self.audio, 16000)
        return None

    def play_api(self):
        audio, sr = librosa.load(self.toWav(self.load_audio(self.get_audio()[0])), sr=16000)
        print(audio)
        sd.play(audio, 16000)
        return None

    def get_level(self):
        if not self.level:
            level = self.database.get_word_level(self.word)[0][0]
            self.level = level
            return level
        else:
            return self.level

    def run(self):
        return [Audio(word=self.word,language=self.language, audio = base64.b64encode(y).decode()) for y in self.get_audio()]


class Audio:
    def __init__(self, word, language, audio):
        self.word = word
        self.audio = audio
        self.deck = language

    def __str__(self):
        return f"('{self.word}','{self.deck}', '{self.audio}')"





if __name__=="__main__":
    word = Word("Ong", "vietnamese")
    print(word.play())
    [print(x) for x in word.run()]





