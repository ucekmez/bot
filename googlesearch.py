'''
Created on May 5, 2017

@url https://github.com/anthonyhseb/googlesearch
@author: anthony
'''

import urllib2
import math
import re
from bs4 import BeautifulSoup
from pprint import pprint
from threading import Thread
from collections import deque
from time import sleep
        
class GoogleSearch:


	# SET VARIABLES
    
    # Set fake user agent
    try:
	    from fake_useragent import UserAgent
	    USER_AGENT = UserAgent().random
	    #print USER_AGENT
    except:
	    print ("Warn : Missing libary; assign static user agent. To install fake user agent library, try command :  \n pip install fake-useragent")
	    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36"
	    pass

	# Set proxy host address
    PROXY_IP = "35.188.230.45" 

    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = ".srg h3.r a"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
    
    def search(self, query, num_results = 10, prefetch_pages = True, prefetch_threads = 10, language = "en"):
        searchResults = []
        pages = int(math.ceil(num_results / float(GoogleSearch.RESULTS_PER_PAGE)));
        fetcher_threads = deque([])
        total = None;
        for i in range(pages) :
            start = i * GoogleSearch.RESULTS_PER_PAGE


			###### Run Proxy
            proxy = urllib2.ProxyHandler({'http': GoogleSearch.PROXY_IP})
            opener = urllib2.build_opener(proxy)
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            urllib2.install_opener(opener)

            response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ urllib2.quote(query) + "&hl=" + language + ("" if start == 0 else ("&start=" + str(start))))

            #print response.fp._sock.fp._sock.getpeername() # print used ip 
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            if total is None:
                totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next().encode('utf-8')
                total = long(re.sub("[',\. ]", "", re.search("(([0-9]+[',\. ])*[0-9]+)", totalText).group(1)))
            results = self.parseResults(soup.select(GoogleSearch.RESULT_SELECTOR))
            if len(searchResults) + len(results) > num_results:
                del results[num_results - len(searchResults):]
            searchResults += results
            if prefetch_pages:
                for result in results:
                    while True:
                        running = 0
                        for thread in fetcher_threads:
                            if thread.is_alive():
                                running += 1
                        if running < prefetch_threads:
                            break
                        sleep(1)
                    fetcher_thread = Thread(target=result.getText)
                    fetcher_thread.start()
                    fetcher_threads.append(fetcher_thread)
        for thread in fetcher_threads:
            thread.join()
        return SearchResponse(searchResults, total);
        
    def parseResults(self, results):
        searchResults = [];
        for result in results:
            url = result["href"];
            title = result.text
            searchResults.append(SearchResult(title, url))
        return searchResults

class SearchResponse:
    def __init__(self, results, total):
        self.results = results;
        self.total = total;

class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.__text = None
        self.__markup = None
    
    def getText(self):
        if self.__text is None:
            soup = BeautifulSoup(self.getMarkup(), "lxml")
            for junk in soup(["script", "style"]):
                junk.extract()
                self.__text = soup.get_text()
        return self.__text
    
    def getMarkup(self):
        if self.__markup is None:
            opener = urllib2.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(self.url);
            self.__markup = response.read()
        return self.__markup
    
    def __str__(self):
        return  str(self.__dict__)
    def __unicode__(self):
        return unicode(self.__str__())
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    import sys
    search = GoogleSearch()
    i=1
    query = " ".join(sys.argv[1:])
    if len(query) == 0:
        query = "python"
    count = 10
    print ("Fetching first " + str(count) + " results for \"" + query + "\"...")
    response = search.search(query, count)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    for result in response.results:
        print("RESULT #" +str (i) + ": "+ (result._SearchResult__text if result._SearchResult__text is not None else "[None]") + "\n\n")
        i+=1
