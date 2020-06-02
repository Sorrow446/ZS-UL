#!/usr/bin/env python3

import os
import re
import sys
import random
import argparse

import requests


try:
	if hasattr(sys, 'frozen'):
		os.chdir(os.path.dirname(sys.executable))
	else:
		os.chdir(os.path.dirname(__file__))
except OSError:
	pass

s = requests.Session()
s.headers.update({
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
				  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
				  "/75.0.3770.100 Safari/537.36",
	'Referer': "https://www.zippyshare.com/"
})

print("""
 _____ _____     _____ __    
|__   |   __|___|  |  |  |   
|   __|__   |___|  |  |  |__ 
|_____|_____|   |_____|_____|
""")

def parse_prefs():
	p = argparse.ArgumentParser()
	p.add_argument(
		'-f', '--files', 
		nargs='+', required=True,
		help='Paths of files to upload separated by a space.'
	)
	p.add_argument(
		'-pv', '--private',
		help='Set uploaded files to private.',
		action='store_true'
	)
	p.add_argument(
		'-p', '--proxy',
		help='HTTPS only. <IP>:<port>.'
	)
	p.add_argument(
		'-o', '--output',
		help='Path of text file to write URLs to.'
	)
	p.add_argument(
		'-n', '--no-wipe',
		help='Don\'t wipe output text file before writing to it.',
		action='store_true'
	)
	args = p.parse_args()
	return args

def dir_setup():
	path = os.path.dirname(cfg.output)
	try:
		os.makedirs(path, exist_ok=True)
	except FileNotFoundError:
		pass

def wipe_txt():
	with open(cfg.output, 'w') as f:
		pass

def write_txt(fname, url):
	with open(cfg.output, 'a+') as f:
		f.write("{}\n{}\n".format(fname, url))
	print("Wrote to: {}.".format(cfg.output))
	
def set_proxy():
	s.proxies.update({'https': 'https://' + cfg.proxy})	

def check_size(abs):
	total = os.path.getsize(abs)
	if total > 524288000:
		raise Exception("File exceeds 500 MB limit.")
	return total

def upload(abs, fname):
	server = random.randint(1, 120)
	total = check_size(abs)
	url = "https://www{}.zippyshare.com/upload".format(server)
	files = {
		'file': open(abs, 'rb')
	}
	if cfg.private:
		files['private'] = "true"
	else:
		files['notprivate'] = "true"
	r = s.post(url, files=files)
	return r.text
	
def extract(html):
	regex = (
		r'onclick=\"this.select\(\);" value="(https://www\d{1,3}'
		r'.zippyshare.com/v/[a-zA-Z\d]{8}/file.html)'
	)
	url = re.search(regex, html)
	if not url:
		raise Exception("Failed to extract URL.")
	return url.group(1)

def main(abs):
	fname = os.path.basename(abs)
	print(fname)
	html = upload(abs, fname)
	url = extract(html)
	print(url)
	if cfg.output:
		write_txt(fname, url)

if __name__ == '__main__':
	cfg = parse_prefs()
	if cfg.output:
		dir_setup()
		if not cfg.no_wipe:
			wipe_txt()
	if cfg.proxy:
		set_proxy()
	total = len(cfg.files)
	for num, abs in enumerate(cfg.files, 1):
		print("\nFile {} of {}:".format(num, total))
		try:
			main(abs)
		except Exception as e:
			print("Failed.")
			print("{}: {}".format(e.__class__.__name__, e))
