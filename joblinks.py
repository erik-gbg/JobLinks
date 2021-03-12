import sys
import os
import json
import requests

"""
Joblinks
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


# This module excludes all hits that comes from Arbetsförmedlingen and only show results from other sources
# the field 'sourceLinks' in the ad is a list of the source(s) where the original ad was found
exclude = 'arbetsformedlingen.se'

# 100 is max number of hits that can be returned.
# If there are more you have to use offset and multiple requests to get all ads
limit = 100


def _get_ads(params):
    headers = {'accept': 'application/json'}
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf8'))


def number_of_hits(query):
    limit = 0
    search_params = {'q': query, 'exclude_source': exclude, 'limit': limit}
    json_response = _get_ads(search_params)
    return json_response['total']['value']


def get_hits_batch(query, limit, offset):
    search_params = {'q': query, 'exclude_source': exclude, 'limit': limit, 'offset': offset}
    json_response = _get_ads(search_params)
    return json_response['hits']


def get_hits_all(query):
    num_hits = number_of_hits(query)
    all_hits = []
    for offset in range(0, num_hits, limit):
        hits = get_hits_batch(query, limit, offset)
        all_hits.extend(hits)
    return all_hits


def list_of_sites(hits):
    sites = set()
    for hit in hits:
        source_links = hit.get('source_links', [])
        for i in range(len(hit['source_links'])):
            sites.add(source_links[i].get('label', '-'))
    return sorted(sites)


# catalogue grouped by sites
def build_ads_catalogue(hits):
    catalogue = {}
    for site in list_of_sites(hits):
        catalogue[site] = []
    for hit in hits:
        source_links = hit.get('source_links', [])
        for i in range(len(source_links)):
            site = source_links[i].get('label', '-')
            ad_dict = {}
            ad_dict['headline'] = hit.get('headline', 'no headline given')
            ad_dict['employer'] = hit.get('employer', {}).get('name', 'no employer name given')
            ad_dict['url'] = source_links[i].get('url', '')

            ad_dict['other_urls'] = []
            for j in range(len(source_links)):
                if j != i:
                    ad_dict['other_urls'].append(source_links[j].get('url', ''))

            addresses = hit.get('workplace_addresses', [])
            if not addresses:
                ad_dict['municipality'] = ['-']
            else:
                ad_dict['municipality'] = []
                for a in range(len(addresses)):
                    ad_dict['municipality'].append(addresses[a].get('municipality', ''))

            catalogue[site].append(ad_dict)
    return catalogue


def filter_only_multihits(hits):
    multi_hits = []
    for hit in hits:
        if len(hit['source_links']) > 1:
            multi_hits.append(hit)
    return multi_hits


def get_ads_catalogue(query):
    return build_ads_catalogue(get_hits_all(query))


def get_ads_catalogue_only_multihits(query):
    return build_ads_catalogue(filter_only_multihits(get_hits_all(query)))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        query = sys.argv[1]
        print(f'Query = "{query}"')
    else:
        query = 'Python'  # default
        print(f'Using default query = "{query}"')

    all_hits = get_hits_all(query)

    ads_catalogue = build_ads_catalogue(all_hits)
    json_filename = query.lower() + " " + "catalogue.json";
    f = open(json_filename, "w", encoding="utf-8")
    json.dump(ads_catalogue, f)
    print("File written:", os.path.realpath(f.name))
    f.close()

    mh_catalogue = build_ads_catalogue(filter_only_multihits(all_hits))
    json_filename = query.lower() + " " + "catalogue multihits.json";
    f = open(json_filename, "w", encoding="utf-8")
    json.dump(mh_catalogue, f)
    print("File written:", os.path.realpath(f.name))
    f.close()



