from bs4 import BeautifulSoup
import sys
import requests
import Queue
from Link import Link
from page_data import page_data
import argparse
import cgi

current_count = 0

def extract_details(url, status, soup):
	details = page_data(url)
	try:		
		details.status = status
		details.title = soup.title.get_text().strip()			
		#details.meta = [cgi.escape(str(y).strip()) for y in soup.find_all('meta')]
		for meta in soup.find_all('meta'):
			if meta.get('name') == 'description':
				details.meta = meta.get('content')
		#extract only meta-description - that's the only one we're interested wrt SEO

		details.h1 = [cgi.escape(y.get_text().strip()) for y in soup.find_all('h1')]		
		details.h2 = [cgi.escape(y.get_text().strip()) for y in soup.find_all('h2')]		
		#print details		
		#print details.json_details()
		print_html(details)
	except Exception as e:
		print >> sys.stderr, 'extract_details:' + str(e)

def print_headers():
	print ''''
<html>
	<head>
		<meta charset="utf-8"/>
		<title>SEO Parser Report</title>
		<style>
			body	{font-family: Helvetica, Sans-Serif;}
			tr:nth-child(even) {background: #b8d1f3;}
			tr:nth-child(odd) {background: #dae5f4;}
		</style>
	</head>
	<body>
		<table border="1">
			<tr><th>URL</th><th>Status</th><th>Meta Tags</th><th>Meta #</th><th>Title</th><th>Title #</title><th>H1</th><th>H2</th></tr>
'''

def print_footers():
	print '</table></body></html>'	

def print_list(objs):
	if len(objs) == 1:
		print objs[0],
	else:
		print '<ul>',
		for obj in objs:
			print '<li>' + obj + '</li>',
		print '</ul>',	

def print_html(details):
	print '<tr>',
	try:
		print '<td>' + details.url + '</td>',
		print '<td>' + str(details.status) + '</td>',

		print '<td>',
		if details.meta:
			print details.meta,
		print '</td>',

		print '<td>',
		if details.meta and len(details.meta) > 0:
			print str(len(details.meta)),
		else:
			print "0",
		print '</td>',

		print '<td>',
		if details.title:
			print details.title,
		print '</td>',

		print '<td>',
		if details.title and len(details.title)>0:
			print str(len(details.title)),
		else:
			print "0",
		print '</td>',

		print '<td>',
		if details.h1:
			print_list(details.h1)
		print '</td>',

		print '<td>',
		if details.h2:
			print_list(details.h2)
		print '</td>',						
	except Exception as e:
		print >> sys.stderr, 'print_html:' + str(e)
	print '</tr>'


	
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
			except KeyError as e:
				print >> sys.stderr, 'Parse:' + str(e)
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
		file_name = 'index.html'
		if args.outfile:
			file_name = args.outfile
		print 'Output will be saved to file ' + file_name
		file_handle = open(file_name, 'w')
		sys.stdout = file_handle		
		print_headers()
		parse(queue, links, domain, protocol, processed)
		print_footers()
		if file_handle:
			file_handle.close()
		sys.stdout = sys.__stdout__
	except Exception as e:
		print >> sys.stderr, 'Main:' + str(e)
	print 'Done.'
