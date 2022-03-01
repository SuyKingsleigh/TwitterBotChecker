import re

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

            print(meta_data_link)
            return meta_data_link


if __name__ == '__main__':
    print(
        TweetHandler('123', 'uga buga https://localhost banana http://www.sourcebits.com/').get_meta_data_from_links())
