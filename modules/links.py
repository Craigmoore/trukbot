#!/usr/bin/env python
import urllib2
import re

title = ""

class LinksParser():
	def Page(self, url):
		request = urllib2.Request(url=url)
		opener = urllib2.urlopen(request)
		data = opener.read()
		opener.close()
		self.Regex(data)

	def Regex(self, page):
		research = re.search(r'<title>.*<\/title>', page, re.I)
		title = research.group(0)
		title = re.sub('<\/?title>', '', title)
		if research:
			global title	
			title = title
		else:
			print "This page has no title."

	def Main(self, page):
		page = re.sub('https:', 'http:', page, re.I)
		httpcheck = re.search(r'http\:\/\/', page, re.I)
		if httpcheck:
			try:	
				self.Page(page)
			except Exception as e:
				print e
		else:
			try:
				url = 'http://' + page
				self.Page(url)
			except Exception as e:
				print e