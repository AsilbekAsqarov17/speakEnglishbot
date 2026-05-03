import requests
import json
from pprint import pprint as print
import os


app_id = os.getenv("OXFORD_APP_ID")
app_key = os.getenv("OXFORD_APP_KEY")
language = "en-gb"

def getDefinitions(word_id):
    url = "https://od-api-sandbox.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    res = r.json()
    if 'error' in res.keys():
        return False

    output = {}
    senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']

    definitions = []
    for sense in senses:
        definitions.append(f"{sense['definitions'][0]}")

    output['definitions'] = " ".join(definitions)

    if res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0].get('audioFile'):
        output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

    return output

if __name__ == "__main__":
    print(getDefinitions('ace'))
    print(getDefinitions('Great Britain'))
