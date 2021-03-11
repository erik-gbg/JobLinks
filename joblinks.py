import requests
import json

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
    for offset in range(0, num_hits, 100):
        hits = get_hits_batch(query, limit, offset)
        all_hits.extend(hits)
    return all_hits


def list_of_sites(hits):
    sites = []
    for hit in hits:
        for i in range(len(hit['source_links'])):
            sites.append(hit['source_links'][i]['label'])
    return sorted(set(sites))


# catalogue grouped by sites
def build_ads_catalogue(hits):
    catalogue = {}
    for site in list_of_sites(hits):
        catalogue[site] = []
    for hit in hits:
        for i in range(len(hit['source_links'])):
            site = hit['source_links'][i]['label']
            ad_dict = {}
            ad_dict['headline'] = hit['headline']
            ad_dict['employer'] = hit['employer']['name']
            ad_dict['url'] = hit['source_links'][i]['url']
            # ad_dict['brief'] = hit['brief']
            try:
                ad_dict['municipality'] = hit['workplace_addresses'][0]['municipality']
            except:
                ad_dict['municipality'] = ''
            try:
                ad_dict['region'] = hit['workplace_addresses'][0]['region']
            except:
                ad_dict['region'] = ''
            other_urls = []
            for j in range(len(hit['source_links'])):
                if j != i:
                    other_urls.append(hit['source_links'][j]['url'])
            ad_dict['other_urls'] = other_urls
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
    try:
        query = sys.argv[1]
    except:
        query = 'Python'  # default

    all_hits = get_hits_all(query)

    ads_catalogue = build_ads_catalogue(all_hits)
    json_filename = query.lower() + " " + "catalogue.json";
    f = open(json_filename, "w", encoding="utf-8")
    json.dump(ads_catalogue, f)
    f.close()

    mh_catalogue = build_ads_catalogue(filter_only_multihits(all_hits))
    json_filename = query.lower() + " " + "catalogue multihits.json";
    f = open(json_filename, "w", encoding="utf-8")
    json.dump(mh_catalogue, f)
    f.close()


