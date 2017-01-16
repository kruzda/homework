#!/usr/bin/env python2

from __future__ import print_function
import urllib
import json

r = urllib.urlopen("http://198.61.207.112/output")
rr = json.loads(r.read())

try:
	count = int(rr[0]['count'])
	text = str(rr[0]['text'])
except e:
	print(str(e))

l = 1

print("input: {0}\ncount: {1}\ntext: {2}\n".format(json.dumps(rr, indent=2) ,count, text))
print("----5---10---15---20---25---30---35---40---45---50---55---60---65---70")

for i in text:
	print(i, end="")
	if not l % count:
		l = 1
		print("")
	else:
		l += 1

print("")
