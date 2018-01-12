#!/usr/bin/env python2

import urllib
import urllib2
import io
from bs4 import BeautifulSoup
import json
import time
import gmplot

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

		timeout_start = time.time()
		while time.time() < timeout_start + timeout:
			# tmpRestaurant[ "coordinates" ] = gmap.geocode(restaurantName.encode('ascii','replace') + " geneva, switzerland")
			try:
				tmpRestaurant[ "coordinates" ] = gmap.geocode(restaurantName.encode('ascii','replace') + " geneva, switzerland")
				tmpRestaurant[ "valid" ] = True
				break
			except:
				continue

		getRestaurantSite(restaurantName.encode('ascii','replace') )

		tmpRestaurant[ "address" ] = ""
		tmpRestaurant[ "categories" ] = []
		tmpRestaurant[ "tripAdvisorLink" ] = ""
		tmpRestaurant[ "yelpLink" ] = ""
		tmpRestaurant[ "description" ] = ""

		listOfRestaurantObjects.append(tmpRestaurant)
		if i>max:
			break

	return listOfRestaurantObjects


def getRestaurantSite(name="",site="TripAdvisor"):
	query = urllib.urlencode({'q' : "%s %s"%(name.encode('ascii','replace'),site)})
	print(query)
	# response = urllib2.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	# jsonResponse = json.loads ( response )
	# print jsonResponse
	# results = jsonResponse [ 'responseData' ] [ 'results' ]
	# print results
	# for result in results:
	#     title = result['title']
	#     url = result['url']   # was URL in the original and that threw a name error exception
	#     print ( title + '; ' + url )


if __name__ == "__main__":
	listOfRestaurants = []
	scrapeAssiette(listOfRestaurants)
	listOfRestaurantObjects = getMetaData(listOfRestaurants,max=5)

	with open('restaurantDB.json', 'w') as outfile:
	    json.dump(listOfRestaurantObjects, outfile)



