#!/usr/bin/env python2

from __future__ import print_function
import io

import gmplot
import time

import json

from collections import namedtuple

# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

# timeout variable can be omitted, if you use specific value in the while condition
timeout = 2   # [seconds]


# class restaurantObject(object):
# 	def __init__(self,name):
# 		self.name = name
# 		self.coordinates = (0,0)
# 		self.valid = False

# 		timeout_start = time.time()
# 		while time.time() < timeout_start + timeout:
# 			try:
# 				self.coordinates = gmap.geocode(name.encode('ascii','replace') + " geneva")
# 				self.valid = True
# 				break
# 			except:
# 				continue
# 		self.address = ""
# 		self.categories = []
# 		self.tripAdvisorLink = ""
# 		self.yelpLink = ""
# 		self.description = ""
# 		return

class Map(object):
	def __init__(self):
		self._points = []
		self.centerLat, self.centerLon = 0,0
	def add_point(self, restaurant ):
		self._points.append( restaurant )
	def set_center(self, x, y):
		self.centerLat = x
		self.centerLon = y
	def makeDescription(self,restaurant):
		try:
			description = \
			"""{address} <br> \
			{phone} <br><br> \
			{rating} Stars on TripAdvisor <br> \
			Price: {price} <br><br> \
			{cuisines} <br><br> \
			<a target='_blank' href='{tripAdvisorLink}'>TripAdvisor</a> \
			""".format(
				address = restaurant.address.encode('ascii', 'xmlcharrefreplace'),
				phone = restaurant.phone.encode('ascii', 'xmlcharrefreplace'),
				rating = restaurant.rating.encode('ascii', 'xmlcharrefreplace'),
				price = restaurant.price.encode('ascii', 'xmlcharrefreplace'),
				cuisines = ", ".join([x.encode('ascii', 'xmlcharrefreplace') for x in restaurant.cuisine]),
				tripAdvisorLink = restaurant.tripAdvisorLink.encode('ascii', 'xmlcharrefreplace')
				)
		except:
			description = "No TripAdvisor Information"

		return description

	def __str__(self):
		markersCode = "\n".join(
			[
			"""

			marker = new google.maps.Marker({{
				position: new google.maps.LatLng({lat}, {lon}),
				map: map,
				clickable: true,
				title: "{name}"
				}});

			google.maps.event.addListener(marker, 'click', ( function(marker,i) {{
				return function() {{
					infowindow.setContent("<h3>{name}</h3> {description}");
					infowindow.open(map, marker);
				}}
			}})(marker,i) );

			i = i+1

			""".format(
				lat=restaurant.coordinates[0],
				lon=restaurant.coordinates[1],
				name=restaurant.name.encode('ascii', 'xmlcharrefreplace'),
				description=self.makeDescription(restaurant)	) for restaurant in self._points
			]
			)
		return """
			<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDOxxf9lLj8lGEfrThmIaQHCm07WYfUiIk"></script>
			<div id="map-canvas" style="height: 100%; width: 100%"></div>
			<script type="text/javascript">
				var map;
				function show_map() {{
					map = new google.maps.Map(
						document.getElementById("map-canvas"),
						{{
							zoom: 13,
							center: new google.maps.LatLng({centerLat}, {centerLon})
						}}
					);

					var infowindow = new google.maps.InfoWindow();
					var marker, i
					i=0

					{markersCode}

				}}
				google.maps.event.addDomListener(window, 'load', show_map);
			</script>
		""".format(centerLat=self.centerLat, centerLon=self.centerLon,
				   markersCode=markersCode)


if __name__ == "__main__":

	gmap = gmplot.GoogleMapPlotter(0,0,10)
	genevaCoordinates = (46.2044, 6.1432)
	map = Map()
	map.set_center(*genevaCoordinates)

	jsonDB = json.load(open('restaurantDB.json'))

	# print(gmap.geocode("clubhouse geneva")  )

	for item in jsonDB:
		# print(item["address"].encode('ascii','replace') + " geneva")
		# item["coordinates"] = gmap.geocode(item["address"].encode('ascii','replace') + " geneva")
		# item["coordinates"] = gmap.geocode("clubhouse geneva")
		print(item.keys() )
		if "coordinates" not in item.keys():
			continue
		restaurant = namedtuple('X', item.keys())(*item.values())
		print(restaurant.name.encode('ascii', 'xmlcharrefreplace'))
		# if restaurant.valid:
		map.add_point( restaurant )

	# with io.open('listOfRestaurants.txt','r', encoding='utf-8', errors='replace') as f:
	# 	for i,line in enumerate(f):
	# 		restaurant = restaurantObject(line.strip())
	# 		print(restaurant.name.encode('ascii', 'xmlcharrefreplace'))
	# 		if restaurant.valid:
	# 			map.add_point( restaurant )
	# 		# map.add_point( restaurantObject("Holy Cow") )

	with open("index.html", "w") as out:
		print(map, file=out)



