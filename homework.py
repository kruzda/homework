#!/usr/bin/env python2

from __future__ import print_function
import urllib
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action="store_true", help="enable verbose output")
parser.add_argument('-m', '--mode', default='greedy', choices=['simple', 'greedy', 'minrag'], help="select which mode to use to break text")
args = parser.parse_args()

try:
	r = urllib.urlopen("http://198.61.207.112/output")
except Exception as e:
	print("connection problem: {}".format(str(e)))	
	exit(1)

rr = r.read()

try:
	rrr = json.loads(rr)
except Exception as e:
	print("invalid json received: {}".format(rr))
	exit(1)

try:
	count = int(rrr[0]['count'])
	text = str(rrr[0]['text'])
except Exception as e:
	print("invalid data received: {}".format(json.dumps(rrr, indent=2)))
	exit(1)

def v_print(msg):
	if args.verbose:
		print(msg)

v_print("input:\n {0}\ncount: {1}\ntext: {2}".format(json.dumps(rrr, indent=2) ,count, text))
v_print("line beaking mode: {}\n".format(args.mode))
v_print("----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90")

if args.mode == "simple":

	l = 1

	for char in text:
		print(char, end="")
		if not l % count:
			l = 1
			print("")
		else:
			l += 1
	print("")


elif args.mode == "greedy":

	currLine = ""

	for word in text.split():
		if count < len(currLine) + len(word):
			if 0 < len(currLine):
				print(currLine)
				currLine = ""
			while count < len(word):
				print(word[:count-1:] + "-")
				word = word.split(word[:count:])[1]
		currLine += word + " "
	print(currLine)


elif args.mode == "minrag":

	width = count
	words = text.split()
	count = len(words)

	slack = [[0] * count for i in range(count)]
	for i in range(count):
		slack[i][i] = width - len(words[i])
		for j in range(i + 1, count):
			slack[i][j] = slack[i][j - 1] - len(words[j]) - 1
	minima = [0] + [10 ** 20] * count
	breaks = [0] * count
	for j in range(count):
		i = j
		while 0 <= i:
			if slack[i][j] < 0:
				cost = 10 ** 10
			else:
				cost = minima[i] + slack[i][j] ** 2
			if cost < minima[j + 1]:
				minima[j + 1] = cost
				breaks[j] = i
			i -= 1

	lines = []
	j = count
	while 0 < j:
		i = breaks[j - 1]
		lines.append(' '.join(words[i:j]))
		j = i
	lines.reverse()

	for line in lines:
		print(line)

else:
	print("no such mode: {}".format(args.mode))
