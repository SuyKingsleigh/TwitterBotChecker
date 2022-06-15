import re

from src.FactCheckerClient import FactCheckerClient
from src.MetaDataAnalyzer import MetaDataAnalyzer
from src.db.Tweet import Tweet


class TweetHandler:
    def __init__(self, id, text):
        self._id = id
        self._text = text

    def handle_when_no_link(self):
        print('handle_when_no_link() handling tweet without link: ' + self._text)

        self._text = self._text.split(" ")
        param_list = []

        for param in self._text:
            if len(param) > 0 and param[0] != '@':
                param_list.append(param)

        return FactCheckerClient(param_list).check()

    def has_links(self):
        return len(self.find_links()) > 0

    def _get_by_id(self):
        pass

    def get_tweet(self) -> Tweet:
        try:
            return Tweet(tweet_id=self._id, text=self._text, link=self.find_links_as_string())
        except Exception as e:
            print(e)
            return Tweet(tweet_id=self._text, text=self._text, link=self._text)

    def find_links_as_string(self):
        ", ".join(self.find_links())

    # Retornara um array contendo todos os links de um tweet
    def find_links(self):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, self._text)
        return [x[0] for x in url]

    # Tentara extrair os metadados de um link
    def get_meta_data_from_links(self):
        links = self.find_links()
        if len(links) > 0:
            meta_data_link = {}

            for link in links:
                try:
                    meta_data_link[link] = MetaDataAnalyzer(link).get_meta_from_link()
                except:
                    print('could not find metadata from ' + link)
                    meta_data_link[link] = None

            return meta_data_link

    def handle(self):
        claims = self.get_meta_data_from_links()
        for link in claims.keys():
            if link is None:
                print("invalid link")
                continue

            print('verifying url: ' + link + ' keywords: ' + str(claims[link]))
            fact_checker_client = None

            if claims[link]:
                if claims[link]['content']:
                    fact_checker_client = FactCheckerClient(claims[link]['content'])
                elif claims[link]['title']:
                    fact_checker_client = FactCheckerClient(claims[link]['title'])
                else:
                    print('could not retrieve any useful info')
                    return None
            else:
                fact_checker_client = FactCheckerClient([link])

            checked = fact_checker_client.check()
            if checked['data']:
                return checked['data']
            else:
                return None


if __name__ == '__main__':
    print(TweetHandler('123',
                       'Olha que louco isso ai  https://www.ndtv.com/world-news/ghost-of-kyiv-real-or-urban-legend-some-facts-about-ukraines-ace-2795817').handle())
