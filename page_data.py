import json

class page_data:

	def __init__(self, url):
		self.url = url
		self.status = 0
		self.meta = []
		self.h1 = []
		self.h2 = []
		self.title = None

	def __str__(self):
		obj = {}
		obj['url'] = self.url
		obj['status'] = self.status
		obj['title'] = self.title
		obj['meta'] = self.meta
		obj['h1'] = self.h1
		obj['h2'] = self.h2
		return str(obj)

	def json_details(self):
		obj = {}
		obj['url'] = self.url
		obj['status'] = self.status
		obj['title'] = self.title
		obj['meta'] = self.meta
		obj['h1'] = self.h1
		obj['h2'] = self.h2
		return json.dumps(obj)

	def print_details(self):
		strbuffer = 'URL: ' + self.url + "\n"
		strbuffer = 'Status ' + self.status + "\n"
		if self.title != None:
			strbuffer += 'Title: ' + self.title + "\n"		
		if len(self.meta) > 0:
			strbuffer += 'Meta: '+ ",".join(self.meta) + "\n"
		if len(self.h1) > 0:
			strbuffer += 'H1: '+ ",".join(self.h1) + "\n"
		if len(self.h2) > 0:
			strbuffer += 'H2: '+ ",".join(self.h2) + "\n\n"
		return strbuffer