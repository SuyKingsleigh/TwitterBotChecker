# Classe para representar um tweet
class Tweet:
    # tweet_id
    # text
    # link (default null)
    def __init__(self, tweet_id, text, link):
        self.tweet_id = tweet_id
        self.text = text
        self.link = link
