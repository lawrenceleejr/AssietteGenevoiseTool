#!/usr/bin/env python2

from __future__ import print_function
import gmplot



class restaurantObject(object):
	def __init__(self,name):
		self.name = name
		while(1):
			try:
				self.coordinates = gmap.geocode(name + " geneva")
				break
			except:
				continue
		self.address = ""
		self.categories = []
		self.tripAdvisorLink = ""
		self.yelpLink = ""
		self.description = ""
		return

class Map(object):
	def __init__(self):
		self._points = []
		self.centerLat, self.centerLon = 0,0
	def add_point(self, restaurant ):
		self._points.append( restaurant )
	def set_center(self, x, y):
		self.centerLat = x
		self.centerLon = y
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
					infowindow.setContent("{name} {name}");
					infowindow.open(map, marker);
				}}
			}})(marker,i) );

			i = i+1

			""".format(
				lat=restaurant.coordinates[0],
				lon=restaurant.coordinates[1],
				name=restaurant.name,
				description="\n".join([restaurant.name,"test"]) )  for restaurant in self._points
			]
			)
		return """
			<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
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

	map.add_point( restaurantObject("Clubhouse") )
	map.add_point( restaurantObject("Holy Cow") )

	with open("output.html", "w") as out:
		print(map, file=out)



