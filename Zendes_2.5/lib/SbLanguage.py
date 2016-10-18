#-*- coding: utf-8 -*-
''' Language package-loader for game "Zendes 2.5" https://vk.com/zendes25'''
''' from russian developer MihailRis '''
''' YouTube: https://www.youtube.com/channel/UC_2jkzD35jeM4kR3y5Saf4w '''

''' '''

#_version_ = 0.1

def load(lang):
	lang_dict = {}
	lang1 = []
	if type(lang) == list:
		lang1 = lang
	elif type(lang) == file:
		lang1 = lang.readlines()

	if lang1 == []:
		raise TypeError
	for l in lang1:
		if not l.startswith("#") and not l.startswith("%") and len(l) > 4:
			data = l.split("=")
			lang_dict[data[0]] = data[1][:-1]

	return lang_dict
