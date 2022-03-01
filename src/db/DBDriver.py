# Classe para se comunicar com o db
import mysql.connector
import os
from dotenv import load_dotenv

from src.db.Mention import Mention
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
    def insert(tweet):
        insert = """INSERT INTO Tweet (tweet_id, text, link) values (%s, %s, %s)"""

        with DBDriver(commit=True) as driver:
            driver.cursor.execute(insert, (tweet.tweet_id, tweet.text, tweet.link))

    @staticmethod
    def find_by_id(tweet_id):
        return TweetDao._find_by_id((tweet_id,))

    @staticmethod
    def _find_by_id(tweet_id):
        select = """SELECT * from Tweet where tweet_id = %s"""

        with DBDriver() as driver:
            driver.cursor.execute(select, tweet_id)

            for (tweet_id, text, link) in driver.cursor:
                return Tweet(tweet_id, text, link)

    @staticmethod
    def find_by_link(link):
        return TweetDao._find_by_link((link,))

    @staticmethod
    def _find_by_link(link):
        select = """SELECT * from Tweet where link = %s"""

        with DBDriver() as driver:
            driver.cursor.execute(select, link)

            tweets = []
            for (tweet_id, text, link) in driver.cursor:
                tweets.append(Tweet(tweet_id, text, link))

            return tweets


class MentionDao:
    @staticmethod
    def insert(mention):
        insert = """INSERT INTO Mention (mention_id, since_id) VALUES (%s, %s)"""
        with DBDriver(commit=True) as driver:
            driver.cursor.execute(insert, (mention.mention_id, mention.since_id))


if __name__ == '__main__':
    print("sup world")
    # tweet = Tweet(tweet_id='123abc', text='texto de teste yay', link='www.google.com')
    # TweetDao.insert(tweet)
    # print(TweetDao.find_by_id('123abc'))
    # for link in TweetDao.find_by_link("www.google.com"):
    #     print(link)

    mention = Mention("1234", "4321", None)
    MentionDao.insert(mention)
