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
from os.path import basename
from functools import reduce

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

def toString(arr):
    return reduce(lambda x, y: x + y if x == '' else x + "," + y.strip(), arr, '')

def main(csvfile):
    with open(csvfile, "r") as f:
        csvreader    = csv.reader(f)
        headline  = csvreader.__next__()
        header    = listToDict(headline)
        count     = 1
        headline += ['locations', 'misc', 'people']
        data      = []
        for line in csvreader:
            content = ""
            content += " " + line[header['keywords']]
            content += " " + line[header['title']]
            content += " " + line[header['summary']]
            content += " " + line[header['metatags_content']]
            tagged = tagCell(content)
            locations   = toString(filterTags(tagged, ["LOCATION"]))
            miscs       = toString(filterTags(tagged, ["MISC"]))
            people      = toString(filterTags(tagged, ["PERSON"]))
            count += 1
            newline = line + [locations, miscs, people]
            data.append(newline)
            print(
                "%s\tOrg lang %s found locs: %s and miscs: %s people: %s" % (
                    count,
                    line[header['language']],
                    locations,
                    miscs,
                    people,
                )
            )


        with open("with_ner_" + basename(csvfile), "w") as f:
            writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writerow(headline)
            writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Just give it a csv file and see how it works!"
    )
    parser.add_argument(
        "csvfile",
        type=str,
        help="csvfile to analyse with stanford NER"
    )

    args = parser.parse_args()

    main(args.csvfile)
