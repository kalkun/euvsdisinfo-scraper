#!/usr/bin/env python3

"""
    This script will help collecting meta data over a collection of URLs.
    The meta data will be based on header tags such as those used for SEO optimizations, title tag or similar.

    The following is an example of describing a wikipedia article on yellow journalism:
    ```
    from collect_article_info import describe_article as da
    da("https://en.wikipedia.org/wiki/Yellow_journalism")
    ```

"""

import requests as req
from bs4 import BeautifulSoup as bs
import json
import csv
import re
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

whitespace = re.compile("(\r|\n|\t|u'\xa0')+")
def rm_whitespace(s): return re.sub(whitespace, " ", s).strip()

def dump_extracts(rows):
    with open("test_extraction.csv", "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
        writer.writerows(rows)

def describe_article(url):
    try:
        page = req.get(url, headers={"User-Agent": "chrome"})
    except:
        return "", ""

    soup = bs(page.content, 'lxml')
    metatags = {}
    for tag in metatag_list:
        try:
            content = ""
            for x in soup.find_all("meta", {tag[0]: tag[1]}):
                content += x[tag[2]]
            if content != "":
                metatags[tag[0] + '_' + tag[1]] = content.strip()
        except:
            print("Failed to find meta tag %s with value %s" % (tag[0], tag[1]))
            continue
    for tag in tag_list:
        try:
            content = ""
            #for x in soup.find(tag[0]):
            x = soup.find(tag[0])
            if not tag[1] is None:
                content += x[tag[1]]
            else:
                content += " " + x.text
            if content != "":
                i = 1
                while tag[0] + "_%s" % i in metatags:
                    i += 1
                metatags[tag[0] + "_%s" % i] = content.strip()
            #print("Could find metatags for tag %s\n%s" % (tag[0], x.text))
        except:
            #print("Could not find metatags for tag %s" % tag[0])
            continue

    tags = ""
    info = ""
    for k, v in metatags.items():
        # collect info gathered in metatags, but try
        # to exclude duplicate information
        v = rm_whitespace(v)
        if (info in v and info != "") or v in info:
            continue
        elif info == "":
            info += v
        elif info[-1] != " ":
            info += " " + v
        else:
            info += v
        tags += k if tags == "" else ", " + k
    print("\t%s" % info)
    return tags.strip(), info

if __name__ == "__main__":
    try:
        with open("./full_dataset_formatted.csv", "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar="\"")
            orig_header = next(reader)
            header = {v: k for k, v in enumerate(orig_header)}
            print(header)
            newRows = [
                orig_header + ["metatags", "metatags_content"] # new header row for new csv
            ]
            for row in reader:
                source = header['source']
                url = row[source]
                print("_" * 80)
                print(url)
                print("\n%s" % row[header['language']])
                newRows.append(row + list(describe_article(url)))
    except KeyboardInterrupt:
        print("Caught interrupt, dumping data")
        dump_extracts(newRows)
        print("Data dumped")
    # if finished, dump data:
    dump_extracts(newRows)

