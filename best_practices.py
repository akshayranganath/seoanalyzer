import requests
from bs4 import BeautifulSoup

def check_best_practices(domain, protocol):
	
	print '<h2>General SEO Best Practices</h2><ul>',
	
	# check for robots.txt
	url = protocol + '://' + domain + '/robots.txt'	
	r = requests.get(url,allow_redirects=False, verify=False)	
	if r.status_code==200:
		print '<li class="good">Robots.txt: Found</li>',	
	else:
		print '<li class="bad">Robots.txt: Not Found</li>',

	# check for sitemap.xml
	url = protocol + '://' + domain + '/sitemap.xml'	
	r = requests.get(url,allow_redirects=False,verify=False)		
	if r.status_code==200:
		'<li class="good">sitemap.xml: Found</li>',	
	else:
		print '<li class="bad">sitemap.xml: Not Found</li>',

	# check for sitemap.xml.gz
	url = protocol + '://' + domain + '/sitemap.xml.gz'	
	r = requests.get(url,allow_redirects=False,verify=False)		
	if r.status_code==200:
		'<li class="good">sitemap.xml.gz: Found</li>',	
	else:
		print '<li class="bad">sitemap.xml.gz: Not Found</li>',		

	# check for sitemap.gz
	url = protocol + '://' + domain + '/sitemap.gz'	
	r = requests.get(url,allow_redirects=False,verify=False)		
	if r.status_code==200:
		'<li class="good">sitemap.xml.gz: Found</li>',	
	else:
		print '<li class="bad">sitemap.xml.gz: Not Found</li>',				

	#fetch the home page response for the rest of analysis
	url = protocol + '://' + domain + '/'
	r = requests.get(url,allow_redirects=False,verify=False)
	soup = BeautifulSoup(r.content, 'lxml')
	
	# check for responsive setup in <meta> tag
	meta_viewport = False
	for meta in soup.find_all('meta'):
			if meta.get('name') == 'viewport':
				meta_viewport = True
				print '<li class="good">Meta-Viewport found: ' + meta.get('content') + '</li>',
	if meta_viewport== False:
		print '<li class="bad">Meta-Viewport is not defined</li>',
	
	# check for unicode content type
	meta_unicode = False
	if 'Content-Type' in r.headers and r.headers['Content-Type'].find('charset') > -1:
		print '<li class="good">Character Encoding detected in response headers.</li>',
		meta_unicode = True
	else:
		for meta in soup.find_all('meta'):
			if meta.get('charset'):
				meta_unicode = True
				print '<li class="good">Character Encoding detected in &lt;meta&gt; tags</li>',
	if meta_viewport== False:
		print '<li class="bad">Charset definition not found.</li>',
	
	# check for language setting
	if soup.get('lang'):
		print '<li class="good">Language details specific in &lt;html&gt; tag.</li>',
	else:
		print '<li class="bad">Language is unspecified in &lt;html&gt; tag.</li>',

	# check for vary:user-agent
	if 'Vary' in r.headers and r.headers['Vary'].find('User-Agent') > -1:
		print '<li class="good"><i>Vary: User-Agent</i> header detected.</li>',
	else:
		print '<li class="bad"><i>Vary: User-Agent</i> header not detected.</li>',

	print '</ul>',
