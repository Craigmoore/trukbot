import urllib2, re, json

ApiURL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="
	
class NowPlaying():
	def __init__(self):
		print "lastfm.py loaded!"

	def main(self, lastfmuser, apikey):
		self.readapi(lastfmuser, apikey)
		return (self.artistName, self.trackName, self.albumName)
	
	def readapi(self, lastfmuser, key):
		api = urllib2.urlopen("%s%s&api_key=%s&format=json" % (ApiURL, lastfmuser, key))
		apidata = api.read()
		api.close()
		self.parsing(apidata)

	def parsing(self, data):
		data = json.loads(data)
		artistName = data["recenttracks"]["track"][0]["artist"]["#text"]
		trackName = data["recenttracks"]["track"][0]["name"]
		albumName = data["recenttracks"]["track"][0]["album"]["#text"]
		self.artistName, self.trackName, self.albumName = artistName.encode("utf-8"), trackName.encode("utf-8"), albumName.encode("utf-8")
