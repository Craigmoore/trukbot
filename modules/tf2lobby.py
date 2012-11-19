#!/usr/bin/env python
import json
import urllib2
import re

API = "http://tf2lobby.com/api/lobbies"
lobbyname = ""
mapname = ""
apidata = ""
lobbyid = ""

class lobbyParser:
	def __init__(self):
		print "tf2lobby.py loaded!"
	
	def main(self, lobby):
		self.parse(lobby)
		self.readapi()
		self.getname(apidata, lobbyid)

	def parse(self, lobby):
		global lobbyid
		lobbyid = re.search(r'(?<==)[0-9]{6}', lobby, re.I)
		lobbyid = lobbyid.group(0)

	def readapi(self):
		try:
			api = urllib2.urlopen(API)
			global apidata
			apidata = api.read()
			api.close()
		except Exception as e:
			print e

	def getname(self, data, lobbyid):
		jsondump = json.loads(data)
		global lobbyname
		global mapname
		for item in jsondump["lobbies"]:
			if item["lobbyId"] == lobbyid:
				lobbyname = item["lobbyName"]
				mapname = item["mapName"]
				lobbyname = lobbyname.encode("utf-8")
				mapname = mapname.encode("utf-8")