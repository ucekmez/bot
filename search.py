# -*- coding: utf-8 -*-
import sys
from lxml import html
import requests
from random import shuffle
reload(sys)
sys.setdefaultencoding('utf8')

from googlesearch import GoogleSearch

term = 'tanrı var mı'
sources = [{'page': 'eksisozluk', 'suffix': 'ekşi', 'case':'?a=nice'},
            #{'page': 'kizlarsoruyor', 'suffix': 'soruyor', 'case':''}
            ]

# combine term and suffixes and create a terms list
terms = [' '.join([term, i['suffix']]) for i in sources]

############ helper functions
def get_source(link, which=None):
    for source in sources:
        if source['page'] in link:
            if which == "case":
                return source['case']
            else:
                return source
    return False


############ helper functions


searches = [GoogleSearch().search(term) for term in terms]
results = []
for search in searches:
    for result in search.results[:3]:
        results.append(result.url + get_source(result.url, "case"))

shuffle(results)

def fetch_link(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)

    if get_source(link)['page'] == "eksisozluk":
        divs = tree.xpath('//div[@class="content"]')
        entries = []
        for div in divs:
            entries.append(div.xpath('text()'))

        shuffle(entries)

        for i in entries[0]:
            print i



fetch_link(results[0])






#
