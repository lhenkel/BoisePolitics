from bs4 import BeautifulSoup
from sets import Set
import ConfigParser, os
import os.path
import pickle
import urllib
import praw
import sys

really_post = True

config = ConfigParser.RawConfigParser()
config.read('boise.cfg')

def post_to_reddit(reddit_obj, title, summary, link, picture = '', style = 'self_post'):
	
	target_sub = 'IdahoPolitics'   ## change to 'test' if testing
	#target_sub = 'test'  
	
	if style == 'self_post':
		summary = summary + "\n\n" + '[>>Full Story](' + link + ')'
	
	got_error = False
	try:
		if style == 'self_post':
			reddit_obj.subreddit(target_sub).submit(title, summary)					 
		else:
			reddit_obj.subreddit(target_sub).submit(title, url=link)					 

	except  (RuntimeError, TypeError, NameError, praw.exceptions.APIException) as err :
		print("Oops! didnt work: ", err)
		got_error = err
		
	return got_error

reddit = praw.Reddit(client_id=config.get('Main', 'client_id'), client_secret=config.get('Main', 'client_secret'), 	password=config.get('Main', 'password'), user_agent=config.get('Main', 'user_agent'), 	username=config.get('Main', 'username') )
previous_urls_file = 'prev_urls.p'

if os.path.isfile(previous_urls_file):
	print "Found Pickle"
	prev_article_set = pickle.load( open( previous_urls_file, "rb" ) )
else:
	print "didnt find pickle"
	prev_article_set = Set()
	
## Loop through Betsy Russels articles and post	
html_doc = 'http://www.spokesman.com/blogs/boise/'
r = urllib.urlopen(html_doc).read()
soup = BeautifulSoup(r, 'html.parser')
articles = soup.find_all('article')

count = 0	
	
for cur_article in articles:
	count = count + 1
	if count > 13:
		break
	
	cur_href = cur_article.find_all("a")[0]["href"]
	cur_title = cur_article.find_all("a")[0].contents[0].encode(sys.stdout.encoding, errors='replace')
	cur_summary = cur_article.find_all("p")[0].contents[0].encode(sys.stdout.encoding, errors='replace')	
	if cur_href.strip() != '' and cur_title.strip() != '':
		cur_href = 'http://www.spokesman.com' + cur_href
		print cur_title
		if cur_href in prev_article_set:
			print "already posted"
		else:
			print "new to me"

			if really_post:
				got_error = post_to_reddit(reddit, cur_title + ' [BR]', cur_summary, cur_href)
				
				if got_error == False:
					prev_article_set.add(cur_href)
					pickle.dump( prev_article_set, open(previous_urls_file, "wb" ) )

				else:
					print 'Post Error:' + got_error 

		print "=================="

print "Looping statesman politics "		
## Loop through Idaho statesman local politics and post	
html_doc = 'http://www.idahostatesman.com/news/politics-government/state-politics/'
r = urllib.urlopen(html_doc).read()
soup = BeautifulSoup(r, 'html.parser')
articles = soup.find_all('article')

count = 0	
	
for cur_article in articles:
	
	if count > 3:
		break
	
	cur_href = cur_article.find_all("a")[2]['href']
	cur_title = cur_article.find_all("a")[2].contents[0].strip().encode(sys.stdout.encoding, errors='replace')

	if len(cur_article.find_all("p")) >= 2:
		cur_summary = cur_article.find_all("p")[1].contents[0].strip().encode(sys.stdout.encoding, errors='replace')	
		count = count + 1
	else:
		continue
	if cur_href.strip() != '' and cur_title.strip() != '':
		print cur_title
		if cur_href in prev_article_set:
			print "already posted"
		else:
			print "new to me"
			if really_post:
				got_error = post_to_reddit(reddit, cur_title + ' [IS]', cur_summary, cur_href)
				
				if got_error == False:
					prev_article_set.add(cur_href)
					pickle.dump( prev_article_set, open(previous_urls_file, "wb" ) )

				else:
					print 'Post Error:' + got_error 

		print "=================="		
	
pickle.dump( prev_article_set, open(previous_urls_file, "wb" ) )
	
