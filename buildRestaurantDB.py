#!/usr/bin/env python2

import urllib
import webbrowser
import urllib2
import io
from bs4 import BeautifulSoup
import json
import time
import gmplot
import requests
import re

timeout = 2


def scrapeAssiette(listOfRestaurants=[],inputPageURL = "http://www.assiettegenevoise.com/restaurants-2-2018"):
	# Get list of restaurants from assiette site
	print("### Scraping Assiette WebPage:")
	print("### ... %s"%inputPageURL)
	print("### ")

	page = urllib2.urlopen(inputPageURL,timeout=5)
	soup = BeautifulSoup(page, 'html.parser')

	name_box = soup.findAll('div', attrs={'class': 'post-title'})

	f=io.open('listOfRestaurants.txt', 'w', encoding='utf8')

	for i,entry in enumerate(name_box):
		print entry.a.contents
		f.write(entry.a.contents[0]+"\n")
		listOfRestaurants.append(entry.a.contents[0])
	f.close()
	return


def getMetaData(listOfRestaurants,max=-1):
	gmap = gmplot.GoogleMapPlotter(0,0,10)

	listOfRestaurantObjects = []
	for i,restaurantName in enumerate(listOfRestaurants):
		print(restaurantName)
		tmpRestaurant = {}
		tmpRestaurant["name"] = restaurantName


		tmpRestaurant[ "coordinates" ] = (0,0)
		tmpRestaurant[ "valid" ] = False

		# timeout_start = time.time()
		# while time.time() < timeout_start + timeout:
		# 	# tmpRestaurant[ "coordinates" ] = gmap.geocode(restaurantName.encode('ascii','replace') + " geneva, switzerland")
		# 	try:
		# 		tmpRestaurant[ "coordinates" ] = gmap.geocode(restaurantName.encode('ascii','replace') + " geneva, switzerland")
		# 		tmpRestaurant[ "valid" ] = True
		# 		break
		# 	except:
		# 		continue

		tripAdvisorLink = getRestaurantSite(restaurantName.encode('ascii','replace')+" geneva ", "tripadvisor.com")
		yelpLink = getRestaurantSite(restaurantName.encode('ascii','replace')+" geneva ", "yelp.com")
		# print( getTripAdvisorID(tripAdvisorLink) )

		if tripAdvisorLink.startswith("/url?q="):
			tripAdvisorLink = tripAdvisorLink[7:]

		if tripAdvisorLink:
			getTripAdvisorMetaData(tripAdvisorLink) 

		tmpRestaurant[ "address" ] = ""
		tmpRestaurant[ "categories" ] = []
		tmpRestaurant[ "tripAdvisorLink" ] = tripAdvisorLink
		tmpRestaurant[ "yelpLink" ] = yelpLink
		tmpRestaurant[ "website" ] = ""
		tmpRestaurant[ "description" ] = ""

		listOfRestaurantObjects.append(tmpRestaurant)
		if i>max:
			break

	return listOfRestaurantObjects

def getTripAdvisorID(url):
	chunks = url.split("-")
	for chunk in chunks:
		if re.match("^d[0-9]{6,9}$", chunk):
			return chunk[1:]

def getTripAdvisorMetaData(tripAdvisorLink):
	metadata = {}

	response = requests.get(tripAdvisorLink)
	soup = BeautifulSoup(response.text, 'html.parser')

	metadata["address"] = soup.find('span', attrs={'class': 'street-address'}).text
	# print searchResult
	metadata["rating"] = soup.find('span', attrs={'class': 'ui_bubble_rating'})["content"]
	print metadata

	print soup.find('span', attrs={'class': 'rating_and_popularity'})

	return metadata


def getRestaurantSite(name="",site="tripadvisor.com"):

	text = "%s site:%s"%(name,site)
	text = urllib.quote_plus(text)

	url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAsjWbCCq9HFUmbFwZ2LILXRlQ11do5rvA&cx=017576662512468239146:omuauf_lfve&q="+text

	print url
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser')
	print soup
	searchResults = soup.findAll('div', attrs={'class': 'g'})

	url = ""
	# url = searchResults[0].a["href"]
	for i,entry in enumerate(searchResults):
		if "tripadvisor" in site.lower():
			if "www.tripadvisor.com/Restaurant_Review-" not in entry.a['href']:
				continue
		url = entry.a['href']
		break

	return url


if __name__ == "__main__":
	listOfRestaurants = []
	scrapeAssiette(listOfRestaurants)
	listOfRestaurantObjects = getMetaData(listOfRestaurants,max=5)

	with open('restaurantDB.json', 'w') as outfile:
	    json.dump(listOfRestaurantObjects, outfile)



