#!/usr/bin/env python3

import requests
import urllib
import sys
import csv

from config import appid, secret

def get_access_token():
    api_endpoint = "https://graph.facebook.com/v2.11/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials"
    api_endpoint = api_endpoint % (appid, secret)
    return requests.get(api_endpoint).json()['access_token']

def encode(string):
    return urllib.parse.quote_plus(string)

def pprint(obj, indent=0):
    if indent == 0: print("{")
    for k, v in obj.items():
        print(" " * (indent + 2) + k + " : ", end="")
        if type(v) == dict:
            print("{")
            pprint(v, indent=indent+2)
        else:
            print(v)
    print(" " * indent + "}")

def get_shares(url):
    enc_url = encode(url)
    access_token = get_access_token()
    fields = "og_object{engagement}"
    api_endpoint = "https://graph.facebook.com/v2.11/%s?fields=%s&access_token=%s"
    return requests.get(api_endpoint % (enc_url, fields, access_token)).json()

def make_header(l):
    return { v: k for k, v in enumerate(l) }

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise ValueError("Wrong number of arguments")
    # file name must be first argument:
    csvfile = sys.argv[1]
    new_data = []
    with open(csvfile, 'r') as f:
        csvreader = csv.reader(f)
        origin_header = csvreader.__next__()
        header = make_header(origin_header)
        new_header = origin_header + ['likes']
        new_data.append(new_header)
        c = 0
        requests.packages.urllib3.disable_warnings()
        for line in csvreader:
            c += 1
            source = line[header['source']]
            try:
                src_url = requests.get(source, verify=False).url
                shares = get_shares(src_url)
                count = shares['og_object']['engagement']['count']
                new_line = line + [count]
                new_data.append(new_line)
                print("%s) Source %s was liked %s times" % (c, src_url, count))
            # except (KeyError, requests.exceptions.ChunkedEncodingError, requests.exceptions.TooManyRedirects):
            except:
                new_line = line + ['']
                new_data.append(new_line)
                print("%s) Source %s wasn't liked" % (c, src_url))
    with open("with_liked_count_" + csvfile.replace("/", ""), "w") as f:
        csvwriter = csv.writer(f, delimiter=";")
        csvwriter.writerows(new_data)



# {'og_object': {'id': '1440780102703929', 'engagement': {'social_sentence': '52 people like this.', 'count': 52}}, 'id': 'https://tvzvezda.ru/news/vstrane_i_mire/content/201710030853-nx7c.htm'}
