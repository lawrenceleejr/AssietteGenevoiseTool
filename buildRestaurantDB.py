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

	page = urllib2.urlopen(inputPageURL,timeout=10)
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

		tripAdvisorLink = getRestaurantSite(restaurantName.encode('ascii','replace')+" geneva ", "tripadvisor.com")
		yelpLink = getRestaurantSite(restaurantName.encode('ascii','replace')+" geneva ", "yelp.com")

		if tripAdvisorLink:
			metadata = getTripAdvisorMetaData(tripAdvisorLink)
			for item in metadata:
				tmpRestaurant[item] = metadata[item]

		tmpRestaurant[ "tripAdvisorLink" ] = tripAdvisorLink
		tmpRestaurant[ "yelpLink" ] = yelpLink

		listOfRestaurantObjects.append(tmpRestaurant)
		if i>max and max!=-1:
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
	metadata["rating"] = soup.find('span', attrs={'class': 'ui_bubble_rating'})["content"]
	metadata["price"] = soup.find('span', attrs={'class': 'rating_and_popularity'}).text
	metadata["cuisine"] = soup.find('span', attrs={'class': 'header_links rating_and_popularity'}).text.split(", ")
	metadata["phone"] = soup.find('div', attrs={'class': 'phone'}).text

	return metadata


def getRestaurantSite(name="",site="tripadvisor.com"):

	text = "%s site:%s"%(name,site)
	text = urllib.quote_plus(text)

	url = "https://www.startpage.com/do/dsearch?query="+text

	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser')

	searchResults = soup.findAll('div', attrs={'class': 'result'})

	url = ""
	for i,entry in enumerate(searchResults):
		tmpURL = entry.h3.a["href"]
		if "tripadvisor" in site.lower():
			if "www.tripadvisor.com/Restaurant_Review-" not in tmpURL:
				continue
		url = tmpURL
		break

	return url


if __name__ == "__main__":
	listOfRestaurants = []
	scrapeAssiette(listOfRestaurants)
	listOfRestaurantObjects = getMetaData(listOfRestaurants,max=-1)

	with open('restaurantDB.json', 'w') as outfile:
	    json.dump(listOfRestaurantObjects, outfile)



