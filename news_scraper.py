#!/usr/bin/env python3

import sys
import time
import re
import csv
from bs4 import BeautifulSoup as bs
import requests as req
import argparse

def get_case(url):
    time.sleep(0.5)
    print("Fetching %s " % url)
    html = req.get(url)
    soup = bs(html.text, 'lxml')
    r = re.compile('[0-9]+')
    fields = {}

    fields['title'] = soup.find("h2").text.strip()
    main_info = soup.find("div", class_="report-main-info")
    fields['summary'] = main_info.find("div", class_="report-summary-text").text.strip()
    fields['disproof'] = main_info.find("div", class_="report-disproof-text").text.strip()
    fields['source'] = main_info.find("div", class_="report-disinfo-link").find("a").attrs['href']

    meta_info = soup.find("div", class_="report-meta-info").find_all("div", class_="report-meta-item")
    for m in meta_info:
        meta_name = m.find("b").text
        meta_field = m.find(["span", "a"]).text.strip()
        if "Reported in" in meta_name:
            issue = r.search(meta_field)
            if issue is None:
                fields['issue'] = "N/A"
            else:
                fields['issue'] = issue.group()
        elif "Date" in meta_name:
            fields['date'] = meta_field
        elif "Language" in meta_name:
            fields['language'] = meta_field
        elif "Country" in meta_name:
            fields['origin'] = meta_field
        #elif "Reported by" in meta_name:
        #    fields['reported by'] = meta_field
        elif "Keywords" in meta_name:
            fields['keywords'] = meta_field
        elif "Outlet" in meta_name:
            fields['outlet'] = meta_field

    print("\n>>%s<<" % fields['title'])
    print("_" * 80)
    return fields


def get_all_cases(url=None, start_pos=0, end_pos=4000):
    if url is None:
        url = 'https://euvsdisinfo.eu/disinformation-cases/?offset=%s'
    cases = []
    for page in range(start_pos, end_pos, 10):
        time.sleep(1)
        print("Get page: %s" % (url % page))
        page_html = req.get(url % page)
        soup = bs(page_html.text, 'lxml')
        case_links = soup.find_all("div", class_='disinfo-db-cell cell-title')[1:]
        for link in [ x.find('a').attrs['href'] for x in case_links ]:
            cases.append(link)

    print("Number of cases found: %s" % len(cases))
    return cases


def build_dataset(csvfile, offset=None, pages=None):
    args = {}
    if not offset is None:
        args['start_pos'] = offset
    if not pages is None:
        args['end_pos'] = pages*10 + (offset if offset else 0)

    case_links = get_all_cases(**args)
    data = []
    csv_header = [
        'issue',
        'date',
        'outlet',
        'language',
        'origin',
        # 'reported by', does not seem to exist anymore
        'keywords',
        'source',
        'title',
        'summary',
        'disproof',
    ]

    print("_" * 80)
    for link in case_links:
        try:
            fetched = get_case(link)
            row = [ fetched[field] for field in csv_header ]
            data.append(row)
        except Exception as e:
            print("Failed to load resource: %s " % link)


    with open(csvfile, 'w') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
        writer.writerows([csv_header] + data)






if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A scraper for the fake news available at euvsdisinfo.eu"
    )
    parser.add_argument(
        'csvfile',
        metavar='csv',
        type=str,
        help="The csv file to write output to"
    )
    parser.add_argument(
        '-o',
        '--offset',
        metavar='o',
        type=int,
        help='The offset page to start scraping news'
    )
    parser.add_argument(
        '-p',
        '--pages',
        metavar='p',
        type=int,
        help='The number of pages to fetch, each page includes at most 10 fake news cases.'
    )

    args = parser.parse_args()

    build_dataset(**vars(args))
    print("Done")
