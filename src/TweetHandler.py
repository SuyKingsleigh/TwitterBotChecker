import re

from src.FactCheckerClient import FactCheckerClient
from src.MetaDataAnalyzer import MetaDataAnalyzer


class TweetHandler:
    def __init__(self, id, text):
        self._id = id
        self._text = text

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
                       'uga buga  https://www.ndtv.com/world-news/ghost-of-kyiv-real-or-urban-legend-some-facts-about-ukraines-ace-2795817').handle())
