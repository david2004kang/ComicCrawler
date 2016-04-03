#! python3

import re
from html import unescape

from ..core import Episode, grabhtml
from ..safeprint import safeprint

cookie = {}
domain = ["chan.sankakucomplex.com"]
name = "Sankaku"
noepfolder = True
config = {
	"cf_clearance": "請輸入Cookie中的cf_clearance"
}

def loadconfig():
	cookie.update(config)

def gettitle(html, url):
	title = re.search(r"<title>/?(.+?) \|", html).group(1)
	return "[sankaku] " + title

def getepisodelist(html, url, last_episode):
	s = []
	base = re.search("(https?://[^/]+)", url).group(1)
	while True:
		for m in re.finditer(r'href="(/(?:[^/]*/)?post/show/(\d+))"', html):
			url, pid = m.groups()
			e = Episode(pid, base + url)
			if last_episode and last_episode.url == e.url:
				return s[::-1]
			s.append(e)

		m = re.search('next-page-url="([^"]+)"', html)
		if not m:
			break
		u = unescape(m.group(1))
		safeprint(base + u)
		html = grabhtml(base + u)
	return s[::-1]

def getimgurls(html, url):
	u = re.search('href="([^"]+)" id=highres', html)
	if not u:
		u = re.search('embed src="([^"]+)"', html)
	return ["https:" + u.group(1)]
