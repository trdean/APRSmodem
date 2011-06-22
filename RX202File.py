#/usr/bin/env python

import bellFileRX, AXParse

d = bellFileRX.Demodulate(8000, 36)
data = d.demod()
#print [n for n in data]

parse = AXParse.AXParser(data)
