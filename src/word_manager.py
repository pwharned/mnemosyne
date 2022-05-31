
from src.db.database import DatabaseManager
from src.word import Word
import sqlite3
import datetime
class WordManager:
    def __init__(self, words, language):
        self.words  = words
        self.database = DatabaseManager()
        self.language = language
        self.date = str(datetime.datetime.now())


    def insert(self):
        words = [Word(x, self.language) for x in self.words]
        audio = [x.run() for x in words]

        words = [f"('{x.word}', '{x.get_translation()}', '{x.language}', 0, '{self.date}')" for x in words]


        audio  = [str(item) for sublist in audio for item in sublist]
        try:
            print(self.database.execute(statement=self._insert_words(words)))
            print(self.database.execute(statement=self._insert_audio(audio)))
        except sqlite3.IntegrityError as error:
            print(error)


    def _insert_words(self, list):
        return f"INSERT INTO WORDS VALUES {','.join(list)}"
    def _insert_audio(self, list):
        return f"INSERT INTO AUDIO VALUES {','.join(list)}"


    def get_words(self, language):

        return self.database.retrieve(f"SELECT W.WORD, W.TRANSLATION, W.LEVEL,W.NEXT_STUDY, W.DECK, A.AUDIO FROM WORDS  as W, AUDIO as A JOIN AUDIO ON LOWER(W.WORD)=LOWER(A.WORD) where W.DECK = '{language.lower()}' ")



if __name__=="__main__":
    words = ["ông", "y tá"]
    manager = WordManager(words, "vietnamese")
    print(manager.insert())

    print(manager.get_words("vietnamese"))
