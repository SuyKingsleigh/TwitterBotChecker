import requests
import json
from main import FACT_CHECK_URL

url = "http://localhost:42042/checkPretty?ghost%kiev"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


class FactCheckerClient:
    def __init__(self, key_words):
        self._key_words = key_words

    def _build_query(self):
        return "%".join(self._key_words)

    def _build_url(self, pretty=False):
        if pretty:
            return FACT_CHECK_URL + "checkPretty?" + self._build_query()
        else:
            return FACT_CHECK_URL + "check?" + self._build_query()

    def check(self):
        response = requests.request("GET", self._build_url(pretty=True), headers={}, data={})
        return response.text


if __name__ == '__main__':
    # print(FactCheckerClient(['ghost', 'kiev']).check())
    j = json.loads(FactCheckerClient(['ghost', 'kiev']).check())
    for r in j['data']:
        print("\n" + r + "\n")