import urllib2
import re
from time import sleep
from xml.dom.minidom import parseString

trackName = ""
artistName = ""
albumName = ""

	
class NowPlaying():
	def __init__(self):
		print "lastfm.py loaded!"

	def main(self, lastfmuser):
		self.readapi(lastfmuser)
		seconds = 1
		sleep(1)
		seconds += 1
		if seconds % 30 == 0:
			self.readapi(lastfmuser)
	
	def readapi(self, lastfmuser, apikey):
		api = urllib2.urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + lastfmuser + '&api_key=' + apikey)
		apidata = api.read()
		api.close()
		self.parsing(apidata)

	def parsing(self, data):		
		dom = parseString(data)
		xmltrackName = dom.getElementsByTagName('name')[0].toxml()
		xmlartistName = dom.getElementsByTagName('artist')[0].toxml()
		xmlalbumName = dom.getElementsByTagName('album')[0].toxml()
		
		global trackName
		trackName = xmltrackName.replace('<name>', '').replace('</name>', '')
		trackName = trackName.replace('&amp;', '&')
		trackName = trackName.encode("utf-8")
		global artistName
		artistName = xmlartistName.replace('</artist>', '')
		artistName = re.sub('.artist.{0,45}>', '', artistName)
		artistName = artistName.replace('&amp;', '&')
		artistName = artistName.encode("utf-8")
		global albumName
		albumName = xmlalbumName.replace('</album>', '')
		albumName = re.sub('.album.{0,45}>', '', albumName)
		albumName = albumName.encode("utf-8")
