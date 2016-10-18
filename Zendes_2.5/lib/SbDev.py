# -*- coding: utf-8 -*-
#DEVILOPER'S TOOLS
import os
import time
import datetime
from shutil import rmtree
from os import listdir, makedirs
from os.path import isdir, isfile
import pygame
from SbConstants import *
import math

start_game_dev = (2016, 5, 18)

REGION_SISE = 32

def dist(x1,x2, y1,y2):
	k = ((x2-x1)**2 + (y2-y1)**2); #Формула расстояния между двумя точками
	k1 = math.sqrt(k)
	return k1

def toogle(value):
	if type(value) == bool:
		if value:
			return False
		else:
			return True
	if type(value) == int:
		if value == 1:
			return False
		if value == 0:
			return True


class Delay():
	def __init__(self):
		self.frames = 0
		self.all = 0

	def update(self):
		self.frames += 1
		self.all += 1

	def get(self):
		frames = self.frames
		return self.frames

	def remove(self):
		self.frames = 0

	def set(self, number):
		self.frames = number


def game_life():
	a = datetime.datetime.now()
	b = datetime.datetime(2016, 5, 18, 0, 0, 00)
	c = a - b
	print(str(c.days)+" дней игре")
game_life()


def sb_output(gmpath, data, consol=True, dop_output="output"):
	OutPutPath = gmpath+"/"+dop_output
	if not os.path.isdir(OutPutPath):
		os.mkdir(OutPutPath)
	if consol:
		print(data)
	str_time = time.ctime()
	spaceb = "|_____|"
	day = str(list(time.localtime())[0])+"_"+str(list(time.localtime())[1])+"_"+str(list(time.localtime())[2])
	pth = OutPutPath+"/output_%s.log" % day
	if not os.path.isfile(pth):
		with open(pth, 'w') as Outfile:
			Outfile.write(("#"*bs)+"\n2D_SandBox game output %s:\n" % day +("#"*bs)+"\n\n")
	with open(pth, 'a') as Outfile:
		Outfile = open(pth, 'a')
		if data == "":
			Outfile.write("\n")
		else:
			Outfile.write("|"+str_time+spaceb+data+"\n")

#DIVIS_GET
def divis_get(intnum, divnum):
	if intnum / divnum == float(int(intnum / divnum)):
		return True
	else:
		return False
#REGION_GET
def region_get(x, y):
	x_reg = str(int((x) / REGION_SISE))
	y_reg = str(int((y) / REGION_SISE))
	return (x_reg+"_"+y_reg)

#print(region_get(1900,1100))
#print(REGION_SISE*REGION_SISE)



################################################################################################'''

def Collide(mob, mobs, blocks):
#	not_collable = [0,7,8]
	width = mob.data["sise"][0]
	height = mob.data["sise"][1]

#	mob.onground = False
	try:
		for block in blocks:
			block = blocks[block]
			# DONW BLOCK
			if mob.x >= block.x and mob.x < block.x+bs:
				if mob.y+height <= block.y and mob.y+height+5 >= block.y:
					if block.data.collable:
						mob.yvel = 0
						mob.onground = True
					else:
						mob.onground = False
			if block.data.collable:
				if dist(mob.x, block.x, mob.y, block.y) <= 4*bs:
					# RIGHT BLOCK
					if mob.x < block.x and mob.x+width > block.x-2:
						if int(mob.y) >= block.y-10 and int(mob.y)+height <= block.y+bs+2:
							if mob.xvel > 0.0:
								mob.xvel = -abs(mob.xvel)
							if mob.onground:
								mob.yvel = -3.0
								mob.y += -2
							mob.x = block.x-width
					# LEFT BLOCK
					if mob.x > block.x-5 and mob.x < block.x+bs+3:
						if int(mob.y) >= block.y-10 and int(mob.y)+height <= block.y+bs+2:
							if mob.xvel < 0.0:
								mob.xvel = abs(mob.xvel)
							if mob.onground:
								mob.yvel = -3.0
								mob.y += -2
							mob.x = block.x+bs
					# HEAD BLOCK
					if mob.x > block.x and mob.x < block.x+bs-6:
						if mob.y > block.y and mob.y < block.y+bs:
							mob.damage(0)
		if not mob.onground:
			mob.yvel += 0.3

		mob.x += mob.xvel
		mob.y += min(mob.yvel, 5.0)

	except KeyError:
		pass



#################################################################

def liner(point0, point1, point2):
	point1to2 = point2-point1
	point0to1 = point0-point1
	point2to0 = point2-point0

	percent1 = float(point0to1)/float(point1to2)
	percent2 = float(point2to0)/float(point1to2)

	return (percent1, percent2)

