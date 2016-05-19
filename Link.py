class Link:	

	def __init__(self, url, depth):
		self.depth = depth
		self.url = url

	def get_url(self):
		return self.url

	def get_depth(self):
		return self.depth