from bs4 import BeautifulSoup
import requests


class MetaDataAnalyzer:
    def __init__(self, link):
        self._link = link

    def _string_to_list(self, str):
        try:
            return str.split(", ")
        except:
            return [str]

    def get_meta_from_link(self):
        r = requests.get(self._link)
        soup = BeautifulSoup(r.content, features="html.parser")

        title = soup.title.string
        print('\t\t\tMetaDataAnalyzer: TITLE IS :', title)

        meta = soup.find_all('meta')

        try:
            for tag in meta:
                if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
                    print('\t\t\t\tMetaDataAnalyzer: NAME    :', tag.attrs['name'].lower())
                    print('\t\t\t\tMetaDataAnalyzer: CONTENT :', tag.attrs['content'])

                    return {
                        "title": title,
                        "content": self._string_to_list(tag.attrs['content'])
                    }
        except:
            return {
                "title": title,
                "content": [None]
            }


if __name__ == '__main__':
    print(MetaDataAnalyzer("http://www.sourcebits.com/").get_meta_from_link())
