import requests
import json
from pprint import pprint as print
import os

def getDefinitions(word_id):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_id.lower()}"

    try:
        r = requests.get(url)
        res = r.json()
    except Exception:
        return False
    if isinstance(res, dict) and res.get('title'):
        return False

    data = res[0]
    output = {}
    definitions = []

    for meaning in data.get('meanings', []):
        for sense in meaning.get('definitions', []):
            definitions.append(sense['definition'])

    output['definitions'] = "\n".join(definitions)

    output['audio'] = None
    for phonetic in data.get('phonetics', []):
        if phonetic.get('audio'):
            output['audio'] = phonetic['audio']
            break

    return output

if __name__ == "__main__":
    print(getDefinitions('ace'))
    print(getDefinitions('Great Britain'))
