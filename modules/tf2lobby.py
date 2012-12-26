#!/usr/bin/env python
import json, urllib2, re

API = "http://tf2lobby.com/api/lobbies"

class lobbyParser:
	def __init__(self):
		print "tf2lobby.py loaded!"
	
	def main(self, lobby):
		self.parse(lobby)
		self.readapi()
		self.getname(self.apidata, self.lobbyid)
		return (self.lobbyname, self.mapname, self.missingclasses, self.numpeople, self.maxpeople)

	def parse(self, lobby):
		lobbyid = re.search(r'(?<==)[0-9]{6}', lobby, re.I)
		self.lobbyid = lobbyid.group(0)

	def readapi(self):
		try:
			api = urllib2.urlopen(API)
			self.apidata = api.read()
			api.close()
		except Exception as e:
			print e

	def getname(self, data, lobbyid):
		jsondump = json.loads(data)
		for item in jsondump["lobbies"]:
			if item["lobbyId"] == self.lobbyid:
				self.lobbyname = item["lobbyName"]
				self.mapname = item["mapName"]
				missingclasses = item["openClasses"]
				self.missingclasses = ', '.join(missingclasses)

				numpeople = item["inLobby"]
				self.numpeople = len(numpeople)
				self.maxpeople = item["maxPlayers"]
