import requests
import json

"""
Code from Erik for the assignment given.
Prints ad's URL, or URLs if many.
"""

# The URL of the API is not for public use, you need to set it here
# or put it in the file joblinks.url
URL = ""

if URL == "":
    try:
        f = open("joblinks.url", "r")
        URL = f.read()
        f.close()
    except:
        print("Error: You need to set the correct URL in the code or in the file joblinks.url")
        exit()

def _get_ads(params):
    headers = {'accept': 'application/json'}
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf8'))


def test_filter_source():
    query = 'Python'
    exclude = 'arbetsformedlingen.se'
    limit = 100
    search_params = {'q': query, 'limit': limit, 'exclude_source': exclude}
    json_response = _get_ads(search_params)
    hits = json_response['hits']
    for hit in hits:
        print(f"{hit['headline']}")
        for i in range(len(hit['source_links'])):
            print(f"{hit['source_links'][i]['url']}")


if __name__ == '__main__':
    test_filter_source()
