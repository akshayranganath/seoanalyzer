from bs4 import BeautifulSoup
import sys
import requests
import Queue
from Link import Link
from page_data import page_data
import argparse

current_count = 0

def extract_details(url, status, soup):
	details = page_data(url)
	try:		
		details.status = status
		details.title = soup.title.get_text().strip()			
		details.meta = [str(y).strip() for y in soup.find_all('meta')]
		details.h1 = [y.get_text().strip() for y in soup.find_all('h1')]
		details.h2 = [y.get_text().strip() for y in soup.find_all('h2')]		
		#print details		
		print details.json_details()
	except Exception as e:
		print >> sys.stderr, url + str(e)		

def print_details(url, soup):
	try:
		print '"' + url + '",',
		print '"' + soup.title.get_text().replace('"','\"') + '",',

		lst = soup.find_all('meta')
		print '"',
		if lst:
			for obj in lst:
				#print ">>>" + str(obj)
				print str(obj).strip().replace('"','\\"'),
		print '",',

		lst = soup.find_all('h1')
		print '"',
		if lst:
			for obj in lst:
				print obj.get_text().strip().replace('"','\\"'),
		print '",',

		lst = soup.find_all('h2')
		print '"',
		if lst:
			for obj in lst:
				print obj.get_text().strip().replace('"','\\"'),
		print '",',
		
		print 
	except Exception as e:
		print >> sys.stderr, e		
	
def parse(queue, links, domain, protocol, processed):	
	
	while queue.empty()!= True:
		link = queue.get()			
		r = requests.get(link.get_url(),allow_redirects=False)
		processed.append(link.get_url())
		#all the rest of processing is for HTML type content only
		if r.headers['Content-Type'].startswith('text') and r.content!= None:
			soup = BeautifulSoup(r.content, 'lxml')
			#print_details(link.get_url(), soup)
			extract_details(link.get_url(), r.status_code, soup)
			ahrefs = soup.find_all('a')		
			# check if the link is relative or absolute		
			try:
				for ahref in ahrefs:			
					ahref = ahref['href']
					url = None					
					#print 'processing: ' + ahref
					if ahref.find(domain) == -1:											
						if ahref.startswith('/') and ahref.startswith('//')==False:																			
							url = protocol + '://' + domain + ahref																				
						elif ahref.startswith('/') and ahref.startswith('//'+domain):
							url = protocol +  ahref					
						#simple links 
						elif ahref[0]!="#" and ahref[0].isalpha() and ahref.startswith('http')==False:							
							url = protocol + '://' + domain + '/' + ahref
					else:
						if ahref.startswith('http://'+domain) or ahref.startswith('https://'+domain):
							url = ahref																		
					
					depth = link.get_depth()
					if url and depth < 5:							
						if url not in links:								
							links[url] = Link(url,depth+1)
							queue.put(links[url])						
			except KeyError as k:
				print >> sys.stderr, k
				pass		

	return				
		

def get_domain(url):
	if url.find('https://') > -1:
		domain = url.split('https://')[1].split('/')[0]
	else:
		if url.find('http://') > -1:
			domain = url.split('http://')[1].split('/')[0]
	return domain

def get_protocol(url):
	if url.startswith('http://'):
		protocol = 'http'
	else:
		protocol = 'https'
	return protocol


if __name__ == "__main__":	
	parser = argparse.ArgumentParser(description="Runs an SEO analysis for a website")
	parser.add_argument("url", help="Markdown file to convert")
	parser.add_argument("-outfile", help="Output from the SEO analysis goes here")	
	args = parser.parse_args()
	print 'Running SEO analysis on ' + args.url + '...'
	l = Link(args.url, 1)
	links = {}
	links[l.get_url()] =  l
	domain = get_domain(l.get_url())
	protocol = get_protocol(l.get_url())
	
	processed = []
	queue = Queue.Queue()
	queue.put(l)
	try:
		file_handle = None
		if args.outfile:
			print 'Output will be saved to file ' + args.outfile
			file_handle = open(args.outfile, 'w')
			sys.stdout = file_handle		
		parse(queue, links, domain, protocol, processed)
		if file_handle:
			file_handle.close()
		sys.stdout = sys.__stdout__
	except Exception as e:
		print >> sys.stderr, str(e)
	print 'Done.'
