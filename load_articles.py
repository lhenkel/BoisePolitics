from bs4 import BeautifulSoup
from sets import Set
import ConfigParser, os
import os.path
import pickle
import urllib
#Somethign

config = ConfigParser.RawConfigParser()
config.read('boise.cfg')

print config.get('Main', 'reddit_user')
exit()

html_doc = 'http://www.spokesman.com/blogs/boise/'
r = urllib.urlopen(html_doc).read()
soup = BeautifulSoup(r, 'html.parser')

#print soup.prettify()[0:1000]

articles = soup.find_all('article')

previous_urls_file = 'prev_urls.p'


if os.path.isfile(previous_urls_file):
	print "Found Pickle"
	prev_article_set = pickle.load( open( previous_urls_file, "rb" ) )
else:
	print "didnt find pickle"
	prev_article_set = Set()


for cur_article in articles:
	cur_href = cur_article.find_all("a")[0]["href"]
	
	cur_title = cur_article.find_all("a")[0].contents[0]
	cur_summary = cur_article.find_all("p")[0].contents[0]	
	if cur_href.strip() != '' and cur_title.strip() != '':
		print cur_title
		if cur_href in prev_article_set:
			print "already posted"
		else:
			print "new to me"
			prev_article_set.add(cur_href)
		print "=================="
	
pickle.dump( prev_article_set, open(previous_urls_file, "wb" ) )
	
#test_article = articles[2]
#test_article.find_all("a")[0]["href"]
#title = test_article.find_all("a")[0].contents[0]
#summary = test_article.find_all("p")[0].contents[0]