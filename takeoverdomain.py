#!/usr/bin/env python 
# vietjovi@gmail.com

from __future__ import print_function

import re
import os
import sys
import time
import getopt
import urllib3
import urlparse
import requests
import io
import mmap

# -- common services
# -- Add new services
# -- {'NAME SERVICE' : {'code':'[300-499]','error':'ERROR HERE'}}
# -- More information: https://github.com/EdOverflow/can-i-take-over-xyz

services = {
	'AWS/S3'          : {'code':'[300-499]','error':r'The specified bucket does not exit'},
	'BitBucket'       : {'code':'[300-499]','error':r'Repository not found'},
	'CloudFront'      : {'code':'[300-499]','error':r'ERROR\: The request could not be satisfied'},
	'Github'          : {'code':'[300-499]','error':r'There isn\'t a Github Pages site here\.'},
	'Shopify'         : {'code':'[300-499]','error':r'Sorry\, this shop is currently unavailable\.'},
	'Desk'            : {'code':'[300-499]','error':r'Sorry\, We Couldn\'t Find That Page'},
	'Fastly'          : {'code':'[300-499]','error':r'Fastly error\: unknown domain\:'},

	'FeedPress'       : {'code':'[300-499]','error':r'The feed has not been found\.'},
	'Ghost'           : {'code':'[300-499]','error':r'The thing you were looking for is no longer here\, or never was'},
	'Heroku'          : {'code':'[300-499]','error':r'no-such-app.html|<title>no such app</title>|herokucdn.com/error-pages/no-such-app.html'},
	'Pantheon'        : {'code':'[300-499]','error':r'The gods are wise, but do not know of the site which you seek.'},
	'Tumbler'         : {'code':'[300-499]','error':r'Whatever you were looking for doesn\'t currently exist at this address.'},
	'Wordpress'       : {'code':'[300-499]','error':r'Do you want to register'},
	'ZenDesk'         : {'code':'[300-499]','error':r'Help Center Closed'},

	'TeamWork'        : {'code':'[300-499]','error':r'Oops - We didn\'t find your site.'},
	'Helpjuice'       : {'code':'[300-499]','error':r'We could not find what you\'re looking for.'},
	'Helpscout'       : {'code':'[300-499]','error':r'No settings were found for this company:'},
	'S3Bucket'        : {'code':'[300-499]','error':r'The specified bucket does not exist'},
	'Cargo'           : {'code':'[300-499]','error':r'<title>404 &mdash; File not found</title>'},
	'StatuPage'       : {'code':'[300-499]','error':r'You are being <a href=\"https://www.statuspage.io\">redirected'},
	'Uservoice'       : {'code':'[300-499]','error':r'This UserVoice subdomain is currently available!'},
	'Surge'           : {'code':'[300-499]','error':r'project not found'},
	'Intercom'        : {'code':'[300-499]','error':r'This page is reserved for artistic dogs\.|Uh oh\. That page doesn\'t exist</h1>'},

	'Webflow'         : {'code':'[300-499]','error':r'<p class=\"description\">The page you are looking for doesn\'t exist or has been moved.</p>'},
	'Kajabi'          : {'code':'[300-499]','error':r'<h1>The page you were looking for doesn\'t exist.</h1>'},
	'Thinkific'       : {'code':'[300-499]','error':r'You may have mistyped the address or the page may have moved.'},
	'Tave'            : {'code':'[300-499]','error':r'<h1>Error 404: Page Not Found</h1>'},
	
	'Wishpond'        : {'code':'[300-499]','error':r'<h1>https://www.wishpond.com/404?campaign=true'},
	'Aftership'       : {'code':'[300-499]','error':r'Oops.</h2><p class=\"text-muted text-tight\">The page you\'re looking for doesn\'t exist.'},
	'Aha'             : {'code':'[300-499]','error':r'There is no portal here \.\.\. sending you back to Aha!'},
	'Tictail'         : {'code':'[300-499]','error':r'to target URL: <a href=\"https://tictail.com|Start selling on Tictail.'},
	'Brightcove'      : {'code':'[300-499]','error':r'<p class=\"bc-gallery-error-code\">Error Code: 404</p>'},
	'Bigcartel'       : {'code':'[300-499]','error':r'<h1>Oops! We couldn&#8217;t find that page.</h1>'},
	'ActiveCampaign'  : {'code':'[300-499]','error':r'alt=\"LIGHTTPD - fly light.\"'},

	'Campaignmonitor' : {'code':'[300-499]','error':r'Double check the URL or <a href=\"mailto:help@createsend.com'},
	'Acquia'          : {'code':'[300-499]','error':r'The site you are looking for could not be found.|If you are an Acquia Cloud customer and expect to see your site at this address'},
	'Proposify'       : {'code':'[300-499]','error':r'If you need immediate assistance, please contact <a href=\"mailto:support@proposify.biz'},
	'Simplebooklet'   : {'code':'[300-499]','error':r'We can\'t find this <a href=\"https://simplebooklet.com'},
	'GetResponse'     : {'code':'[300-499]','error':r'With GetResponse Landing Pages, lead generation has never been easier'},
	'Vend'            : {'code':'[300-499]','error':r'Looks like you\'ve traveled too far into cyberspace.'},
	'Jetbrains'       : {'code':'[300-499]','error':r'is not a registered InCloud YouTrack.'},
	
	'Unbounce'        : {'code':'[300-499]','error':r'The requested URL / was not found on this server|The requested URL was not found on this server'},
	'Smartling'       : {'code':'[300-499]','error':r'Domain is not configured'},
	'Pingdom'         : {'code':'[300-499]','error':r'pingdom'},
	'Tilda'           : {'code':'[300-499]','error':r'Domain has been assigned'},
	'Surveygizmo'     : {'code':'[300-499]','error':r'data-html-name'},
	'Mashery'         : {'code':'[300-499]','error':r'Unrecognized domain <strong>'},

}

# -- colors 
r ='\033[1;31m'
g ='\033[1;32m'
y ='\033[1;33m'
b ='\033[1;34m'
r_='\033[0;31m'
g_='\033[0;32m'
y_='\033[0;33m'
b_='\033[0;34m'
e_='\033[0m'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

# -- print
def plus(string): print("{}[+]{} {}{}{}".format(g,e_,g_,str(string),e_))
def warn(string): print("{}[!]{} {}{}{}".format(r,e_,r_,str(string),e_))
def info(string): print("{}[i]{} {}{}{}".format(y,e_,y_,str(string),e_))

def grep(pattern, file_path):
    with io.open(file_path, "r", encoding="utf-8") as f:
        return re.findall(pattern, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))

def request(url,proxy,timeout):
	headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	try:
		req = requests.packages.urllib3.disable_warnings(
			urllib3.exceptions.InsecureRequestWarning
			)
		if proxy:
			req = requests.get(url=url,headers=headers,proxies=proxy,timeout=timeout,allow_redirects=True)
		else:
			req = requests.get(url=url,headers=headers,timeout=timeout,allow_redirects=True)
		return req.status_code,req.content
	except Exception as e:
		pass

	#try https
	url = url.replace("http://","https://")
	plus('Can not connect HTTP! Try HTTPS: %s'%url)
	try:
		req = requests.packages.urllib3.disable_warnings(
			urllib3.exceptions.InsecureRequestWarning
			)
		if proxy:
			req = requests.get(url=url,headers=headers,proxies=proxy,timeout=timeout,allow_redirects=True)
		else:
			req = requests.get(url=url,headers=headers,timeout=timeout,allow_redirects=True)
		return req.status_code,req.content
	except Exception as e:
		pass
	return None,None

def checker(status,content):
	code = ""
	error = ""
	# --
	for service in services:
		values = services[service]
		for value in values:
			opt = services[service][value]
			if value == 'error':error = opt 
			if value == 'code':code = opt 
		# ---
		if re.search(code,str(status),re.I) and re.search(error,str(content),re.I):
			return service,error
	return None,None

def banner():
	print("#> Code by Vietjovi - vietjovi@gmail.com")
	print("-"*40)

def help():
	banner()
	print("Usage: "+sys.argv[0]+" [OPTIONS]\n")
	print("\t-k --keyword\t\tSet keyword (e.g: google)")
	print("\t-d --domain\t\tSet domain (e.g: google.com)")
	print("\t-D --domain-list\tScan multiple targets in a text file")
	print("\t-p --set-proxy\t\tUse a proxy to connect to the target URL")
	print("\t-o --set-output\t\tUse this setting for save a file")
	print("\t-t --set-timeout\tSet a request timeout. Default value is 2 seconds\n")
	print("Example:")
	print("\tpython %s --domain google.com"%(sys.argv[0]))
	print("\tpython %s --keyword google"%(sys.argv[0]))

	sys.exit()

def sett_proxy(proxy):
	info('Setting proxy.. %s'%proxy)
	return {
	'http':proxy,
	'https':proxy,
	'ftp':proxy
	}

def check_path(path):
	try:
		if os.path.exists(path):
			return path
	except Exception as e:
		warn('%s'%e.message)
		sys.exit()

def readfile(path):
	info('Read wordlist.. %s'%(path))
	try:
		return [l.strip() for l in open(check_path(path),'rb')]
	except Exception as e:
		warn('%s'%e)
		sys.exit()

def check_url(url):
	o = urlparse.urlsplit(url)
	if o.scheme not in ['http','https','']:
		warn('Scheme %s not supported!!'%(o.scheme))
		sys.exit()
	if o.netloc == '':
		return 'http://'+o.path
	elif o.netloc:
		return o.scheme + '://' + o.netloc
	else:
		return 'http://' + o.netloc

def main():
	# ---
	set_proxy = None
	set_output = None
	domain = None
	domain_list = None
	set_timeout = 2
	dataDns = '/data/takeoverdomain/domains.dat'
	# ---
	if len(sys.argv) < 2: help()
	try:
		opts,args = getopt.getopt(sys.argv[1:],'k:d:D:p:o:t:',
			['keyword=','domain=','domain-list=','set-proxy=','set-output=','set-timeout='])
	except Exception as e:
		warn("%s"%e.message)
		# time.sleep(1)
		help()
	banner()
	for o,a in opts:
		if o in ('-k','--keyword'):keyword = a
		if o in ('-d','--domain'):domain = a
		if o in ('-D','--domain-list'):domain_list = a
		if o in ('-p','--set-proxy'):set_proxy = sett_proxy(a)
		if o in ('-o','--set-output'):set_output = a
		if o in ('-t','--set-timeout'):set_timeout = int(a)
	# ---

	if set_output:
		file = open(set_output,"wb")
		file.write('Output File\r\n%s\r\n'%("-"*50))
	if domain:
		url = check_url(domain.strip('\n'))	
		try:
			status,content = request(url,set_proxy,set_timeout)
		except Exception as e:
			warn("Can't create request for url %s"%url)
			status = 'None'
			content = 'None'
			# raise e
			pass
		info('Target url: %s - Status: %s'%(url, status))
		service,error = checker(status,content)
		if service and error:
			plus('Found service: %s'%service)
			plus('%s - Status: %s - A potential TAKEOVER vulnerability found!'%domain%status)
			if set_output:
				file.write('HOST    : %s\r\n'%(domain))
				file.write('SERVICE : %s\r\n'%(service))
				file.write('ERRORS  : %s\r\n'%(error))

	elif domain_list:
		plus('Starting scanning...')
		with open(domain_list, 'r') as domains:
			for domain in domains:
				url = check_url(domain.strip('\n'))
				
				try:
					status,content = request(url,set_proxy,set_timeout)
				except Exception as e:
					warn("Can't create request for url %s"%url)
					status = 'None'
					content = 'None'
					# raise e
					pass
				info('Target url: %s - Status: %s'%(url, status))
				service,error = checker(status,content)
				if service and error:
					print('\x1b[6;30;42m' + '[-] Found service: ' + service + '\x1b[0m')
					# plus('Found service: %s'%service)
					# plus('%s - Status: %s - A potential TAKEOVER vulnerability found!'%(domain,status))
					print('\x1b[6;30;42m' + '[-] A potential TAKEOVER vulnerability found! ' + domain.strip('\n') + '\x1b[0m')
					if set_output:
						file.write('HOST    : %s\r\n'%(domain))
						file.write('SERVICE : %s\r\n'%(service))
						file.write('ERRORS  : %s\r\n'%(error))
	else:help()
	if set_output:
		file.close()
try:
	main()
except KeyboardInterrupt as e:
	warn('Interrupt by user!')
	sys.exit()