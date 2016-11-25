from bs4 import BeautifulSoup
import urllib
#Somethign
html_doc = 'http://www.spokesman.com/blogs/boise/'
r = urllib.urlopen(html_doc).read()
soup = BeautifulSoup(r, 'html.parser')

print soup.prettify()[0:1000]

articles = soup.find_all('article')
test_article = articles[2]
test_article.find_all("a")[0]["href"]