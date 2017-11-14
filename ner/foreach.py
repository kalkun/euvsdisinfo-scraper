#!/usr/bin/python3
# format of data input:
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
#    'metatags_content',
#    'locations',
#    'misc',
#    'people',
# ]

import csv

from location_tagger import listToDict



def main(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f, delimiter=",")
        c = 0
        header = None
        for line in reader:
            c += 1
            if c == 1:
                # save header line
                header = listToDict(line)
                print("{\\bf", line[header['title']], "} & {\\bf", line[header['language']], "} & {\\bf", line[header['locations']], "}\\\\")
                continue
            if len(line[header['title']]) < 30 and len(line[header['locations']]):
                print(line[header['title']], "&", line[header['language']], "&", line[header['locations']], "\\\\")
                # print("%s\t\tin %s naming:\t%s" % (line[header['title']], line[header['outlet']], line[header['locations']]))

if __name__ == "__main__":
    main(csvfile="./with_ner_with_extraction.csv")
