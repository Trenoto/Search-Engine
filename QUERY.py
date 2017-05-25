#!/usr/bin/python
import pickle
with open('m2.pickle','rb') as handle:
	b = pickle.load(handle)
	for key in b:
		if key == 'authors':
			print(b['authors'])
	print(len(b['authors']))
	print(len(b))