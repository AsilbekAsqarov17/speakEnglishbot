import requests
import json
from pprint import pprint as print
import os

def getDefinitions(word_id):
    # Free Dictionary API endpoint (No app_id or app_key required)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_id.lower()}"

    try:
        r = requests.get(url)
        res = r.json()
    except Exception:
        return False

    # The API returns a dictionary with a 'title' if the word is not found
    if isinstance(res, dict) and res.get('title'):
        return False

    # Navigate the Free Dictionary API response structure
    data = res[0]
    output = {}
    definitions = []

    # Extract definitions from all meanings (noun, verb, etc.)
    for meaning in data.get('meanings', []):
        for sense in meaning.get('definitions', []):
            definitions.append(sense['definition'])

    # Format definitions as a single string (joined by newlines for better readability)
    output['definitions'] = "\n".join(definitions)

    # Extract the first available audio file from phonetics
    output['audio'] = None
    for phonetic in data.get('phonetics', []):
        if phonetic.get('audio'):
            output['audio'] = phonetic['audio']
            break  # Stop at the first valid audio link found

    return output

if __name__ == "__main__":
    print(getDefinitions('ace'))
    print(getDefinitions('Great Britain'))
