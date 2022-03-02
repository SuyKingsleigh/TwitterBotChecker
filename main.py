import traceback
from time import sleep

import tweepy
import os
from dotenv import load_dotenv

from src.TweetHandler import TweetHandler
from src.db.DBDriver import MentionDao, TweetDao, ResponseDao, TweetResponseDao
from src.db.Response import Response
from src.db.Tweet import Tweet

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKENS_SECRET = os.getenv('ACCESS_TOKENS_SECRET')
MY_USER_ID = os.getenv('MY_USER_ID')
FACT_CHECK_URL = os.getenv("FACT_CHECK_URL")

client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKENS_SECRET
)


def post_tweet(text, reply_to):
    return client.create_tweet(text=text, in_reply_to_tweet_id=reply_to)


def get_param(src, key, def_value=None):
    try:
        return src[key]
    except:
        return def_value


def handle_mentions(since_id=None):
    last_mention = MentionDao.get_last_mention()

    if not since_id and last_mention:
        since_id = last_mention.mention_id

    print("Checking mentions since_id: " + str(since_id))

    try:
        # retorna um array
        # [0] -> [Tweet{id, text} ...]
        # [3] -> {oldest_id, newest_id, result_count}
        mentions = client.get_users_mentions(id=MY_USER_ID,
                                             since_id=since_id,
                                             user_auth=True)

        oldest_id = get_param(mentions[3], 'oldest_id', 'not_found')
        newest_id = get_param(mentions[3], 'newest_id', since_id)

        if mentions[0]:
            if len(mentions[0]) > 0:
                print('\tFound ' + str(len(mentions[0])) + " new mentions!")
                for m in mentions[0]:
                    print("\t\t handling tweet  {'id': '" + str(m.id) + "' 'text': '" + m.text + "'}")

                    handler = TweetHandler(str(m.id), m.text)
                    if not handler.has_links():
                        print("Could not find links, checking thread ...")
                        thread = client.get_tweet(id=str(m.id), user_auth=True, expansions=['referenced_tweets.id'])
                        original_tweet = thread.includes['tweets'][0]['data']

                        handler = TweetHandler(str(original_tweet['id']), original_tweet['text'])

                    try:
                        tweet = handler.get_tweet()
                        if tweet:
                            TweetDao.insert(tweet)

                        response = handler.handle()
                        if response:
                            for msg in response:
                                print('replying to: ' + str(m.id) + " with: " + msg)
                                post_tweet(msg, str(m.id))
                                resp = ResponseDao.insert(Response(text=msg))
                                TweetResponseDao.insert(str(m.id), resp.response_id)

                    except Exception:
                        print(traceback.format_exc())

        print("Sleeping for 5secs ...")

        sleep(5)
        handle_mentions(since_id=newest_id)
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    print("Starting server with env variables: \n\n" +
          "\n\tCONSUMER_KEY: " + CONSUMER_KEY +
          "\n\tCONSUMER_SECRET: " + CONSUMER_SECRET +
          "\n\tACCESS_TOKEN: " + ACCESS_TOKEN +
          "\n\tACCESS_TOKEN_SECRET: " + ACCESS_TOKENS_SECRET +
          "\n\tMY_USER_ID: " + MY_USER_ID + "\n\n\n\n"
          )

    handle_mentions()
    # r = client.get_tweet(id='1498503958100426752', user_auth=True, expansions=['referenced_tweets.id'])
    # if r.includes:
    #     original_tweet = r.includes['tweets'][0]['data']
    #     print(original_tweet['id'])
    #     print(original_tweet['text'])
