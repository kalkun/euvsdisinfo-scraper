#!/usr/bin/env python3
# See README.md for starting the Stanford Core NLP server
# and example usage.
# CSV header is assumed to be:
# ```
# [
#    'issue',
#    'date',
#    'outlet',
#    'language',
#    'origin',
#    'reported by',
#    'keywords',
#    'source',
#    'title',
#    'summary',
#    'disproof',
#    'metatags',
#    'metatags_content'
# ]
# ```

from nltk.tag.stanford import CoreNLPNERTagger
import argparse
import csv


url = "http://localhost:9000"
ner = CoreNLPNERTagger(url=url)

def tagCell(string):
    return ner.tag(string.split())

def listToDict(l):
    return { x: i for i, x in enumerate(l) }

def uniqueLocations(tags):
    return list(set(map(lambda x: x[0], tags)))

def filterTags(tags, label=["LOCATION"]):
    return uniqueLocations(filter(lambda x: x[1] in label, tags))



def main(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        header = listToDict(reader.__next__())
        count = 1
        for line in reader:
            content = ""
            content += " " + line[header['keywords']]
            content += " " + line[header['title']]
            content += " " + line[header['summary']]
            content += " " + line[header['metatags_content']]
            tagged = tagCell(content)
            #locations = filterTags(tagged)
            locations   = filterTags(tagged, ["LOCATION"])
            miscs       = filterTags(tagged, ["MISC"])
            people      = filterTags(tagged, ["PERSON"])
            print(
                    "%s\tOrg lang %s found locs: %s and miscs: %s people: %s" % (
                        count,
                        line[header['language']],
                        locations,
                        miscs,
                        people,
                    )
                )
            count += 1

if __name__ == "__main__":
    pass
