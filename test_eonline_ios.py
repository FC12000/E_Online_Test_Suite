#!/bin/python
import urllib2
import logging
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
CONFIG_URL = '' # iOS PROD # Contact Francis for the base
#CONFIG_URL = '' # iOS Staging
LOG_FILE = 'eonline_test_suite.log'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=LOG_FILE, filemode='w')
print "logging to file %s" % LOG_FILE

# Parse the Config and return the list of feeds
def get_feeds(config_source_url):
  
    configData = open_URL_Tree(config_source_url)

    feeds = configData.find("feeds")
    #print feeds[0].attrib, feeds[0].text
    print "Feeds have been found."
    return feeds
    
# Parse the feed and return the list of URLs to test
def get_links(feed_source_url):
    feedLinksOutput = list()
    
    feedData = open_URL_Tree(feed_source_url)
    
    for elem in feedData.iterfind('channel/item/link'):
        #print elem.tag, elem.text
        feedLinksOutput.append(elem.text)
    
    print "Links from the feed have been found."
    return feedLinksOutput

# Open the specified URL and return the data as an Element Tree from the feed
def open_URL_Tree(source_url):
    try:
        print "Opening the URL: ", source_url
        file = urllib2.urlopen(source_url)
    except urllib2.HTTPError, e:
        logging.error("")
        logging.error("FAIL: url %s does not exist." % source_url )
        logging.error("Caught exception %s for url %s " % (e.code, source_url) )
    except: 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.exception("caught exception %s, and obj %s at line number %s" % (exc_type, exc_obj, exc_tb.tb_lineno))
    
    urlData = file.read()
    ETdata = ET.fromstring(urlData)
    print "length of ETdata: ", len(ETdata)
    
    return ETdata
    
# Test if the urls in the feed are working
def test_urls(testLinks):
    for url in testLinks: 
        #Response building....
        print "Running tests for URL: %s" % url
        try: 
            response = urllib2.urlopen(url)
            logging.info("\n\nSUCCESS: url %s does exist.  Continuing tests..." % url)
        except urllib2.HTTPError, e:
            logging.error("")
            logging.error("FAIL: url %s does not exist." % url )
            logging.error("Caught exception %s for url %s " % (e.code, url) )
        except: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.exception("caught exception %s, and obj %s at line number %s" % (exc_type, exc_obj, 
                                exc_tb.tb_lineno))
            #logging.info("FAIL: url %s does not exist." % url)
            continue

# Iterate through feedData (eg. news_videos.xml?pageSize=50)
def find_pandas(article_urls):
    
    print "article_urls type: ", type(article_urls)
    if isinstance(article_urls, list):
        for article in article_urls:
            print "article: ", article
            feedData = open_URL_Tree(article)
            
            #videoType = feedData.find("eonline:e_video")
            videoType = feedData.find("eonline:adkeywords") # Test Prod to see if this works
            print "videoType: ", videoType
    elif isinstance(article_urls , str):
        print "article: ", article_urls
        
        try:
            print "Opening the URL: ", article_urls
            file = urllib2.urlopen(article_urls)
        except urllib2.HTTPError, e:
            logging.error("")
            logging.error("FAIL: url %s does not exist." % article_urls )
            logging.error("Caught exception %s for url %s " % (e.code, article_urls) )
        except: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.exception("caught exception %s, and obj %s at line number %s" % (exc_type, exc_obj,
                                exc_tb.tb_lineno))
    
        urlData = file.read()
        #print "urlData: ", urlData
        feedData = ET.fromstring(urlData)
        
        #feedData = open_URL_Tree(article_urls)
        #print "feedData root: ", feedData.getroot()
        #print "feedData attributes: ", feedData.attrib
        print(len(feedData))
        print "feedData: "
        for item in feedData:
            print item.tag, item.attrib
        #videoType = feedData.find("channel/item/eonline") # Test Prod to see if this works
        videoType = feedData.findall("{http://www.eonline.com/static/xml/xmlns/eonline#}")
        print "videoType: ", videoType
        # Iterfind 'channel/item/eonline' in the article data
        #for elem in feedData.iterfind('channel/item/link'):
            #print "link tag: %s, link text: %s" % (elem.tag, elem.text)
            #test for 'e_video' key vs. 'external_video'

if __name__ == "__main__":
    feedData = get_feeds(CONFIG_URL)
    #print feedData[0].attrib, feedData[0].text
    testLinks = get_links(feedData[1].text)
    #print "testLinks: ", testLinks[0]
    #test_urls(testLinks)
    print "testLinks[0]: ", testLinks[0]
    find_pandas(testLinks[0])
