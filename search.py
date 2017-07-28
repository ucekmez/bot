# -*- coding: utf-8 -*-
import sys
from lxml import html
import requests
from random import shuffle
reload(sys)
sys.setdefaultencoding('utf8')

from googlesearch import GoogleSearch


############ helper functions
def get_source(link, which=None):
    for source in sources:
        if source['page'] in link:
            if which == "case":
                return source['case']
            else:
                return source
        else :
          return ''


############ helper functions


'''
  Search google and top links

  @param list terms :  contain search terms
  @param int limit : result url number

  @return list : url list 

'''
def get_urls_from_google(terms):
    url_list = []

    print ('Searching the term : '+str(terms))
    searches = [GoogleSearch().search(term) for term in terms]


    for response in searches:
        for result in response.results: 
            if len(url_list) < LIMIT: # Get top link which limited
                url_list.append(result.url)
            else :		
                pass

    if (SHUFFLE) : # shuffle url list
        shuffle(url_list)
    
    print ('URL pool : '+'\n'.join(url_list))

    if (len(url_list) < 1) : # problem var bazen bos liste geliyor timeout olabilir
        sleep(1000)		
        get_urls_from_google(terms)

    return url_list


'''
  Connect eksisozluk.com, sort entry as best and parse best content

  @param string : url entry url

	@return string : best entry
'''
def parse_eksi_link(url):	

    # set sukela entry url
    url = url+sources[0]['case']
    print ('Searching Url : '+url) 
    page = requests.get(url) 
    tree = html.fromstring(page.content)

    divs = tree.xpath('//div[@class="content"]')
    entries = []
    for div in divs:
        entries.append(div.xpath('text()'))

    if (SHUFFLE) : 
        shuffle(entries)

    best_entry = ''
    for entry in entries[0]: # Get first entry 
        best_entry = entry

    print (best_entry)
    return best_entry
		

'''
  Connect uludagsozluk.com, return first entry

  @param string : url entry url
'''
def parse_uludag_link(url):	

    print ('Searching Url : '+url) 
    page = requests.get(url) 
    tree = html.fromstring(page.content)

    divs = tree.xpath('//div[@class="entry-p"]')
    entries = []
    for div in divs:
        entries.append(div.xpath('text()'))

    if (SHUFFLE) : 
        shuffle(entries)

    best_entry = ''
    for entry in entries[0]: # Get first entry 
        best_entry = entry

    print (best_entry)
    return best_entry


'''
  Connect uludagsozluk.com, return first entry

  @param string : url entry url
'''
def parse_kizlar_link(url):	

    print ('Searching Url : '+url) 
    page = requests.get(url) 
    tree = html.fromstring(page.content)

    divs = tree.xpath('//div[@class="opinion-body expandable-text"]/p')
    entries = []
    for div in divs:
        entries.append(div.xpath('text()')) # <p itemprop="text"

    if (SHUFFLE) : 
        shuffle(entries)

    best_entry = ''
    best_entry = entries[0] # Get first entry 

    print (best_entry)
    return best_entry


if __name__ == "__main__":

    SHUFFLE = False # Rastgele secim yapsın
    LIMIT = 5 # google search limit; ilk besi alır
    SEARCH_TERM = 'kaktus ve radyasyon'

    sources = [{'page': 'eksisozluk', 'suffix': 'site:'+'eksisozluk.com', 'case':'?a=nice'},
                {'page': 'uludagsozluk', 'suffix': 'site:'+'uludagsozluk.com', 'case':''},
            {'page': 'kizlarsoruyor', 'suffix': 'site:'+'kizlarsoruyor.com', 'case':''}

            ]

    response_set = []
    for source in sources:
        term = SEARCH_TERM+' '+source['suffix']

        url_list = get_urls_from_google(term)
        if 'eksi' in source['page']:
            response_set.append(parse_eksi_link(url_list[0]))
        if 'uludag' in source['page']:
            response_set.append(parse_uludag_link(url_list[0]))
        else:
            response_set.append(parse_kizlar_link(url_list[0]))
		 
    print ('Sonuclar : '+'\n'.join(response_set))


