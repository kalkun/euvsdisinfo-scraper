#!/usr/bin/env python3

"""
    This script will help collecting meta data over a collection of URLs.
    The meta data will be based on header tags such as those used for SEO optimizations, title tag or similar.
"""

import requests as req
from bs4 import BeautifulSoup as bs
import json
import csv
"""
* metatag_list is a list of triples where the first are the key value pairs to
* use as filters for relevant tags, the last is the name of the attribute for which
* we are interested in the content of - if the last value is None, the innerHtml will
* be used.
"""
metatag_list = [
    ("name", "description", "content"),
    ("property" "og:title", "content"),
    ("property", "og:description", "content"),
    ("name", "twitter:title", "content"),
    ("name", "twitter:description", "content"),
    ("name", "language", "content"),
    ("name", "keywords", "content"),
    ("name", "subject", "content"),
    ("name", "topic", "content"),
    ("name", "summary", "content"),
    ("name", "subtitle", "content"),
    ("itemprop", "name", "content"),
    ("itemprop", "description", "content"),
]
tag_list = [ ("h%s" % i, None) for i in range(1, 7) ] + [("title", None)]

def describe_page(url):
    page = req.get(url)
    soup = bs(page.text, 'lxml')
    info = {}
    for tag in metatag_list:
        try:
            content = ""
            for x in soup.find_all("meta", {tag[0]: tag[1]}):
                content += x[tag[2]]
            if content != "":
                info[tag[0] + '_' + tag[1]] = content.strip()
        except:
            print("Failed to find meta tag %s with value %s" % (tag[0], tag[1]))
            continue
    for tag in tag_list:
        try:
            content = ""
            for x in soup.find_all(tag[0]):
                if not tag[1] is None:
                    content += x[tag[1]]
                else:
                    content += " " + x.text
            if content != "":
                i = 1
                while tag[0] + "_%s" % i in info:
                    i += 1
                info[tag[0] + "_%s" % i] = content.strip()
        except:
            print("Could not find info for tag %s" % tag[0])
            continue
    print("{")
    for k, v in info.items():
        print("\t%s :\t%s," % (k, v))
    print("}")
    return info

if __name__ == "__main__":
    with open("./first_data.csv", "r") as f:
        reader = csv.reader(f, delimiter=";", quotechar="\"")
        header = {v: k for k, v in enumerate(next(reader))}
        print(header)
        for row in reader:
            source = header['source']
            url = row[source]
            print("_" * 80)
            print(url)
            description = describe_page(url)
#            print(row[header['source']])
#            describe_page(row[header[

