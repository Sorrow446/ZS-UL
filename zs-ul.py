#!/usr/bin/env python3
import os
import re
import sys
import random
import argparse
import mimetypes
import traceback

import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


def walk_path(path):
	for root, _, fnames in os.walk(path):
		for fname in fnames:
			yield os.path.join(root, fname)

def filter_paths(paths):
	filtered = []
	for path in paths:
		if path in filtered:
			print("Filtered duplicate input path \"{}\".".format(path))
		else:
			filtered.append(path)
	return filtered
	
def parse_prefs():
	to_add = []
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-p', '--paths',
		help='Paths to look in for files to upload. Files in nested paths will also '
			 'be added.',
		nargs='+', required=True
	)
	parser.add_argument(
		'--private',
		action='store_true',
		help='Set uploaded files to private.',		
	)
	parser.add_argument(
		'--proxy',
		help='HTTPS only. <IP>:<port>.'
	)
	parser.add_argument(
		'-o', '--output',
		help='Path of text file to write URLs to. Customizable with the template arg.'
	)
	parser.add_argument(
		'-w', '--wipe',
		action='store_true',
		help='Wipe output text file before writing to it.'	
	)
	parser.add_argument(
		'-t', '--template',
		default='{file_path}\n{file_url}\n',
		help='Output text file template. Vars: file_url, filename, file_path.'
	
	)
	parser.add_argument(
		'-r', '--retries',
		type=int, choices=[0, 1, 2, 3, 4, 5], default=0,
		help='How many times to re-attempt failed uploads.'
	)
	args = parser.parse_args()
	args.paths = filter_paths(args.paths)
	for path in args.paths:
		to_add.extend(walk_path(path))
	if not to_add:
		raise Exception('No files found in specified path(s).')
	args.paths = to_add
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

def parse_template(meta):
	try:
		return cfg.template.format(**meta)
	except KeyError:
		print("Failed to parse output template. Default one will be used instead.")
		return "{filename}\n{file_url}\n".format(**meta)		
	
def write_output(url, fname, path):
	template = parse_template({
		'file_url': url, 'filename': fname, 'file_path': path})
	with open(cfg.output, 'a+') as f:
		f.write(template)
	print("Wrote to \"{}\".".format(cfg.output))
	
def set_proxy():
	s.proxies.update({'https': 'https://' + cfg.proxy})

def get_server():
	r = s.get('https://www.zippyshare.com')
	r.raise_for_status()
	match = re.search(r'var server = \'(www\d{1,3})\';', r.text)
	if not match:
		raise Exception('Failed to extract server number.')
	return match.group(1)
	
def check_size(path):
	total = os.path.getsize(path)
	if total > 524288000:
		raise Exception('File exceeds 500 MB.')
	return total

def get_mime_type(fname):
	mime_type = mimetypes.guess_type(fname)[0]
	if mime_type == None:
		mime_type = "application/octet-stream"
	return mime_type

def upload(path, fname):
	server = get_server()
	total = check_size(path)
	url = "https://{}.zippyshare.com/upload".format(server)
	pb = tqdm(total=total, unit='B', unit_scale=True)
	data = {'name': fname, 'file': (fname, open(path, 'rb'), get_mime_type(fname))}
	if cfg.private == True:
		data['private'] = "true"
	else:
		data['notprivate'] = "true"
	multi = MultipartEncoder(fields=data)
	try:
		monitor = MultipartEncoderMonitor(
			multi, lambda multi: pb.update(monitor.bytes_read - pb.n))
		s.headers.update({'Content-Type': monitor.content_type})
		r = s.post(url, data=monitor)
		r.raise_for_status()
	finally:
		if s.headers.get('Content-Type'):
			del s.headers['Content-Type']
		pb.close()
	return r.text

def extract(html):
	regex = (
		r'onclick=\"this.select\(\);" value="(https://www\d{1,3}'
		r'.zippyshare.com/v/[a-zA-Z\d]{8}/file.html)'
	)
	url = re.search(regex, html)
	if not url:
		raise Exception('Failed to extract file URL.')
	return url.group(1)

def main(path):
	print("--" + path + "--")
	fname = os.path.basename(path)
	html = upload(path, fname)
	url = extract(html)
	if cfg.output:
		write_output(url, fname, path)
	else:
		print(url)

if __name__ == '__main__':
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
	cfg = parse_prefs()
	s.mount('https://', HTTPAdapter(max_retries=cfg.retries))
	if cfg.output:
		dir_setup()
		if cfg.wipe == True:
			wipe_txt_file()
	if cfg.proxy:
		set_proxy()
	total = len(cfg.paths)
	for num, path in enumerate(cfg.paths, 1):
		print("\nFile {} of {}:".format(num, total))
		try:
			main(path)
		except Exception:
			print("Failed to upload file.")
			traceback.print_exc()