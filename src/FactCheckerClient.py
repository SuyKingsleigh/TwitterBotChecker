import os
import re

import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

FACT_CHECK_URL = os.getenv("FACT_CHECK_URL")


class FactCheckerClient:
    def __init__(self, key_words):
        self._key_words = []
        for key_word in key_words:
            key_word = re.sub(' ', '%', key_word)
            k = re.sub('[^A-Za-z0-9]+', '%', key_word)
            self._key_words.append(k)

    def _build_query(self):
        return "%".join(self._key_words)

    def _build_url(self, pretty=False):
        if pretty:
            return FACT_CHECK_URL + "checkPretty?" + self._build_query()
        else:
            return FACT_CHECK_URL + "check?" + self._build_query()

    def check(self):
        url = self._build_url(pretty=True)
        print("calling url `" + url + "`")
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {
                "data": [""],
                "errorCode": response.status_code,
                "error": response.text
            }


if __name__ == '__main__':
    # print(FactCheckerClient(['ghost', 'kiev']).check())
    j = json.loads(FactCheckerClient(['ghost', 'kiev']).check())
    for r in j['data']:
        print("\n" + r + "\n")
