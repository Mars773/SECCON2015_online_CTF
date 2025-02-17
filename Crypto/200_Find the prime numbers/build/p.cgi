#!/usr/bin/env python

import sys
import random
import fcntl
import os
import json
import random
import time

def read_json(name):
	with open(name) as f:
		fcntl.flock(f.fileno(), fcntl.LOCK_EX)
		try:
			v = json.loads(f.read())
		finally:
			fcntl.flock(f.fileno(), fcntl.LOCK_UN)
	return v

def write_json(name, v):
	with open(name, "w") as f:
		fcntl.flock(f.fileno(), fcntl.LOCK_EX)
		try:
			f.write(json.dumps(v))
		finally:
			fcntl.flock(f.fileno(), fcntl.LOCK_UN)
	return

print "Content-Type: text/html"
print
print "<html>"
print "<body>"
print "<pre>"

while 1:
	t = int(time.time())
	w = read_json("access.json")
	e = os.environ["REMOTE_ADDR"]
	if not e in w.keys():
		w.setdefault(e, {})
		w[e].setdefault("outp", "")
		w[e].setdefault("time", 0)
	else:
		if t < w[e]["time"]:
			print w[e]["outp"]
			break
	
	v = read_json("data.json")
	
	a = int(v["p"])
	b = int(v["q"])
	n = (a * b)
	l = (a - 1) * (b - 1)
	r = l
	d = 1
	while 1:
		d = ((n // r + 1) * d) % n
		r = (d * l) % n
		if r == 1:
			break
	while 1:
		x = pow(random.randint(1000000000, 9999999999), n, (n * n))
		o = (pow(n + 1, 1, n * n) * x) % (n * n)
		y = (((pow(o, l, n * n) - 1) // n) * d) % n
		if y == 1:
			break
	c = (pow(n + 1, int(v["num"]), n * n) * x) % (n * n)
	h = (c * o) % (n * n)
	q = "%019d + %019d = %019d" % (c, o, h)
	print q
	
	z = "QUERY_STRING"
	if z in os.environ and os.environ[z] != "":
		if w[e]["time"] < t and os.environ[z] == v["num"]:
			print "SECCON{" + v["flag"] + "}"
		w[e]["time"] = t + 60
		w[e]["outp"] = q
	else:
		w[e]["time"] = t + 3
		w[e]["outp"] = q
	
	write_json("access.json", w)
	
	with open("log.txt", "a") as f:
		fcntl.flock(f.fileno(), fcntl.LOCK_EX)
		try:
			f.write(q + "\n")
		finally:
			fcntl.flock(f.fileno(), fcntl.LOCK_UN)
	break

print "</pre>"
print "</body>"
print "</html>"
