import sqlite3
import os
DATABASE = "data.db"

path = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(path, "data.db")

path = os.path.join(path, "sql/ddl/ddl.sql")


class DatabaseManager:
    def __init__(self):
        self.database = DATABASE
        self.conn = None
        self.start_up()


    def connect(self):
        return sqlite3.connect(DATABASE)

    def execute(self, statement):
        if not self.conn:
            self.conn = self.connect()
            res = self.conn.execute(statement)
            self.conn.commit()
            return res
        else:
            res = self.conn.execute(statement)
            self.conn.commit()
            return res

    def close(self):
        if not self.conn:
            return None
        else:
            self.conn.close()
            self.conn = None
            return None

    def retrieve(self, statement):
        result = []
        res = self.execute(statement).fetchall()
        for x in res:
            result.append(x)
        self.close()
        return result


    def start_up(self):
        with open(path, "r") as file:
            start_up = file.readlines()
        for statement in start_up:
            self.execute(statement)



    def get_words(self, language):

        return self.retrieve(f"SELECT W.WORD, W.TRANSLATION, W.LEVEL,W.NEXT_STUDY, W.DECK, A.AUDIO FROM WORDS  as W, AUDIO as A JOIN AUDIO ON LOWER(W.WORD)=LOWER(A.WORD) where W.DECK = '{language.lower()}' ")

    def get_word_audio(self, word):
        return self.retrieve(f"SELECT W.WORD, A.AUDIO FROM WORDS  as W, AUDIO as A JOIN AUDIO ON LOWER(W.WORD)=LOWER(A.WORD) where LOWER(W.WORD) = '{word.lower()}' ")
