# Classe para se comunicar com o db
import time
from sqlite3 import Date

import mysql.connector
import os
from dotenv import load_dotenv

from src.db.Mention import Mention
from src.db.Response import Response
from src.db.Tweet import Tweet

load_dotenv()


class DBDriver:
    def __init__(self, commit=False):
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASS")
        self._host = os.getenv("DB_HOST")
        self._data_base = os.getenv("DB_NAME")
        self.commit = commit

    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=self._user,
            password=self._password,
            host=self._host,
            database=self._data_base
        )

        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            self.connection.commit()

        self.cursor.close()
        self.connection.close()


class TweetDao:
    @staticmethod
    def insert(tweet: Tweet):
        insert = """INSERT INTO Tweet (tweet_id, text, link) values (%s, %s, %s)"""

        with DBDriver(commit=True) as driver:
            driver.cursor.execute(insert, (tweet.tweet_id, tweet.text, tweet.link))

    @staticmethod
    def find_by_id(tweet_id):
        select = """SELECT * from Tweet where tweet_id = %s"""

        with DBDriver() as driver:
            driver.cursor.execute(select, (tweet_id,))

            for (tweet_id, text, link) in driver.cursor:
                return Tweet(tweet_id, text, link)

    @staticmethod
    def find_by_link(link):
        select = """SELECT * from Tweet where link = %s"""

        with DBDriver() as driver:
            driver.cursor.execute(select, (link,))

            tweets = []
            for (tweet_id, text, link) in driver.cursor:
                tweets.append(Tweet(tweet_id, text, link))

            return tweets


class MentionDao:
    @staticmethod
    def insert(mention: Mention):
        insert = """INSERT INTO Mention (mention_id, since_id) VALUES (%s, %s)"""
        with DBDriver(commit=True) as driver:
            driver.cursor.execute(insert, (mention.mention_id, mention.since_id))

    @staticmethod
    def get_last_mention() -> Mention:
        try:
            query = """SELECT * from Mention ORDER BY id DESC LIMIT 1 """
            with DBDriver() as driver:
                driver.cursor.execute(query, )
                mention = None
                for (id, mention_id, since_id, checked_at) in driver.cursor:
                    mention = Mention(id=id, mention_id=mention_id, since_id=since_id, checked_at=checked_at)

                return mention
        except:
            return None


class ResponseDao:
    @staticmethod
    def insert(response: Response):
        insert = """INSERT INTO Response (text) VALUES (%s)"""

        with DBDriver(commit=True) as driver:
            driver.cursor.execute(insert, (response.text,))
            return Response(response_id=driver.cursor.lastrowid, text=response.text)

    @staticmethod
    def find_by_link(link) -> Response:
        try:
            query = """SELECT * From Response r
                        JOIN TweetResponse TR on r.response_id = TR.response_id
                        JOIN Tweet T on TR.tweet_id = T.tweet_id
                            WHERE T.link = %s
                        """

            with DBDriver() as driver:
                driver.cursor.execute(query, (link,))
                response = None

                for (response_id, text) in driver.cursor:
                    response = Response(response_id=response_id, text=text)

                return response
        except:
            return None


class TweetResponseDao:
    @staticmethod
    def insert(tweet_id: str, response_id: int):
        try:
            insert = """INSERT INTO TweetResponse (tweet_id, response_id) VALUES (%s, %s)"""
            with DBDriver(commit=True) as driver:
                driver.cursor.execute(insert, (tweet_id, response_id))
        except:
            pass


if __name__ == '__main__':
    print("sup world")
    # tweet = Tweet(tweet_id='123abc', text='texto de teste yay', link='www.google.com')
    # TweetDao.insert(tweet)
    # print(TweetDao.find_by_id('123abc'))
    # for link in TweetDao.find_by_link("www.google.com"):
    #     print(link)

    # mention = Mention("1234", "4321", None)
    # MentionDao.insert(mention)
    # print(MentionDao.get_last_mention().checked_at)
    #
    print(ResponseDao.insert(Response(text="uma string sei lá " + str(time.time()))).response_id)
    # TweetResponseDao.insert("123abc", 1)
