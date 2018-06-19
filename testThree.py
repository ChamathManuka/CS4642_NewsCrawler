from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import webbrowser
from lxml import html
import requests
import urllib2
import re
import csv
from datetime import datetime
from datetime import timedelta
import unidecode
import unicodedata

start_date = "2015-11-18"
stop_date = "2018-05-12"
updated_date = "2015-11-16"

start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

news_file = open("newsSundayTimes_8.csv", 'wb')
writer = csv.writer(news_file, delimiter=',')

while start < stop:


	if(start <= datetime.strptime(updated_date, "%Y-%m-%d")):
		try:

			print start.strftime("%Y-%m-%d")
			start = start + timedelta(days=1)		
			#r = requests.get('http://www.sundaytimes.lk/archive/2015-01-01')
			#test = html.fromstring(r.text)
			#print (test);
			print "chamath"
			response = urllib2.urlopen('http://www.sundaytimes.lk/archive/'+start.strftime("%Y-%m-%d"))
			html = response.read()
			print "chamath"
			#print html;
			soup = BeautifulSoup(html, 'html.parser')
			#print (type(soup))
			array = [];
			for tag in soup.findAll("div", {"class" : "col-md-12"}):
				array.append(tag);
				#print (tag.class)
				#print (type(tag));
				#newsHeadings = tag.text;
				#print(newsHeadings)
			#print array[1];
			print "chamath"
			for href in array[1].findAll("a", href = True):
				print "link : " + href["href"]
				print "title : " + href.h4.text
				responseNextPage = urllib2.urlopen(href["href"])
				responseNextPageContent =  responseNextPage.read()
				soupNextPage = BeautifulSoup(responseNextPageContent, 'html.parser')
				detail = "";
				arrayTwo = [];
				for content in soupNextPage.findAll("div", {"class" : "row story"}):
					arrayTwo.append(content);
					#print content;
				#print arrayTwo[0];
				#break;
				detail += arrayTwo.text.strip();
				unicodedata.normalize('NFKD', detail).encode('ascii','replace')
				#detail = unicode(detail.encode("utf-16"))
				if(unicodedata.normalize('NFKD', detail).encode('ascii','replace').endswith("Read more Cafe Spectator")):
					#print "chamath"
					#url = url[:-4]
					detail = detail[:-24];
					#print "detail: " + detail.encode("utf-8");
					print "detail: " + unicodedata.normalize('NFKD', detail).encode('ascii','replace')
					writer.writerow([start.strftime("%Y-%m-%d"), href["href"], unicodedata.normalize('NFKD', href.h4.text).encode('ascii','replace'), unicodedata.normalize('NFKD', detail).encode('ascii','replace')]); 
				else:
					print "detail: " + unicodedata.normalize('NFKD', detail).encode('ascii','replace');
					writer.writerow([start.strftime("%Y-%m-%d"), href["href"], unicodedata.normalize('NFKD', href.h4.text).encode('ascii','replace'), unicodedata.normalize('NFKD', detail).encode('ascii','replace')]); 
			
		except Exception as error:
			continue;
		
		
	else:
		try:
			print start.strftime("%Y-%m-%d")
			response = urllib2.urlopen('http://www.sundaytimes.lk/archive/'+start.strftime("%Y-%m-%d"))
			html = response.read()
			soup = BeautifulSoup(html, 'html.parser')
			array = [];
			for tag in soup.findAll("div", {"class" : "col-md-12"}):
				array.append(tag);
			for href in array[1].findAll("a", href = True):
			
				print "link : " + href["href"]
				print "title : " + href.h4.text
				responseNextPage = urllib2.urlopen(href["href"])
				responseNextPageContent =  responseNextPage.read()
				soupNextPage = BeautifulSoup(responseNextPageContent, 'html.parser')
				for content in soupNextPage.findAll("div", {"class" : "row story"}):
					detail = "";
					for contentPara in content.findAll("p", {"class" : None}):
						detail += contentPara.text.strip();
					unicodedata.normalize('NFKD', detail).encode('ascii','replace')
					if(unicodedata.normalize('NFKD', detail).encode('ascii','replace').endswith("Read more Cafe Spectator")):
						detail = detail[:-24];
						writer.writerow([start.strftime("%Y-%m-%d"), href["href"], unicodedata.normalize('NFKD', href.h4.text).encode('ascii','replace'), unicodedata.normalize('NFKD', detail).encode('ascii','replace')]); 
					else:
						#print "detail: " + unicodedata.normalize('NFKD', detail).encode('ascii','replace');
						writer.writerow([start.strftime("%Y-%m-%d"), href["href"], unicodedata.normalize('NFKD', href.h4.text).encode('ascii','replace'), unicodedata.normalize('NFKD', detail).encode('ascii','replace')]);
			start = start + timedelta(days=1) 
			
		except Exception as error:
			start = start + timedelta(days=1)
			continue;	
		

 
news_file.close();


"""
print(soup.prettify())
value = "";
class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'h4'):
			print (attrs)
			#print (tag);
			#newsHeading = soup.find('h4', {"class": 'arc-text'}).text;
			#if not(newsHeading == value):
			#print (newsHeading)
				#value = newsHeading;

newInstance = MyHTMLParser()
newInstance.feed(soup.prettify())
"""
