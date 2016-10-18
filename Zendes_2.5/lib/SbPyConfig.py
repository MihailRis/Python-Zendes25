#!/usr/bin/python
# coding: utf8
import os

__author__ = "BagasovMihail"
__version__ = 1.0

def type_set(string):
	rrfloat = string.replace(".", "")
	if rrfloat != string:
		if rrfloat.isdigit():
			return float(string)
	if string in ("True", "False"):
		return bool(string)
	if string.isdigit():
		return int(string)
	return string



class ConfigFile(object):
	def __init__(self, cfile):
		if type(cfile) == str:
			self.file = cfile
		else:
			raise TypeError("use ConfigFile(str_object)")
		if not os.path.isfile(cfile):
			open(cfile, 'w').close()
		self.configuration = {}
		self.load()

	def save(self):
		cfile = open(self.file, 'w')
		str_data = ""
		for key in self.configuration:
			str_data += "%s = %s\n" % (key, self.configuration[key])
		cfile.write(str_data)
		cfile.close()

	def load(self):
		cfile = open(self.file, 'r')
		data = cfile.readlines()
		for line in data:
			ldata = line[:-1].split(" = ")
			key = ldata[0]
			value = type_set(ldata[1])
			self.configuration[key] = value


	def __getitem__(self, key):
		return self.configuration[key]

	def __setitem__(self, key, value):
		if type(key) != str:
			raise TypeError("key str type")
		else:
			self.configuration[key] = value

	def __str__(self):
		string = "ConfigFile %s" % self.file
		for key in self.configuration:
			string += ("\n    %s: %s" % (key, self.configuration[key]))
		return string
