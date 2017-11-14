#!/usr/bin/env python3

import requests
import urllib

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


    #pprint(requests.get(api_endpoint % (enc_url, fields, access_token)).json())
