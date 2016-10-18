''' MihailRis interface '''
# -*- coding: utf-8 -*-
import pygame
import sys

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY100 = (100,100,100)

_path = sys.path[0][0:-4]

def _toogle(value):
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

def help(mode="all"):
	if mode == "all":
		print "Witgets: Button"
	if mode == "Button" or mode == "button":
		print "Button(text (unicode_text, sise, x, y), side (tuple), sise (tuple), funcTxt (text), font=\"None\")"

class Button():
	def __init__(self, text, side, sise, funcTxt, dside=(0,0)):
		self.image = pygame.Surface(sise)
		self.image.fill((200,200,200))
		pygame.font.init()
		label = pygame.font.Font(_path+"/resources/FreeSansBold.ttf", int(text[1]*0.7))
		l = label.render(text[0], 1, (0,0,0))
		t = 2
		self.type = "BT"
		self.l = l
		self.label = label
		self.t = t
		self.image2 = pygame.Surface((sise[0]-t, t))
		self.image2.fill((255,255,255))
		self.image3 = pygame.Surface((t, sise[1]-t))
		self.image3.fill((255,255,255))
		self.image4 = pygame.Surface((t, sise[1]-t))
		self.image4.fill((100,100,100))
		self.image5 = pygame.Surface((sise[0]-t, t))
		self.image5.fill((100,100,100))
		self.side = side
		self.image.blit(l, (t+text[2],t+text[3]))
		self.image.blit(self.image2, (0,0))
		self.image.blit(self.image3, (0,0))
		self.image.blit(self.image4, (sise[0]-t,t))
		self.image.blit(self.image5, (t,sise[1]-t))
		self.text_pos = [text[2], text[3]]
		self.sise = sise
		self.func = False
		self.funcTxt = funcTxt
		self.dside = dside
		self.string = text[0]
		self.txtsise = text[1]
		self.language_key = text[0]
		self.freeze = False

	def update(self, click, events):
		self.l = self.label.render(self.string, 1, (0,0,0))
		if not self.freeze:
			mp = pygame.mouse.get_pos()
			if mp[0] > self.side[0]+self.dside[0] and mp[0] < self.side[0]+self.sise[0]+self.dside[0] and mp[1] > self.side[1]+self.dside[1] and mp[1] < self.side[1]+self.sise[1]+self.dside[1]:
				self.image.fill((255,255,255))
				self.image.blit(self.l, (self.t+self.text_pos[0],self.t+self.text_pos[1]))
				self.image.blit(self.image2, (0,0))
				self.image.blit(self.image3, (0,0))
				self.image.blit(self.image4, (self.sise[0]-self.t,self.t))
				self.image.blit(self.image5, (self.t,self.sise[1]-self.t))
				if click:
					self.func = True
					if self.funcTxt == "_exit_":
						sys.exit()
			else:
				self.image.fill((200,200,200))
				self.image.blit(self.l, (self.t+self.text_pos[0],self.t+self.text_pos[1]))
				self.image.blit(self.image2, (0,0))
				self.image.blit(self.image3, (0,0))
				self.image.blit(self.image4, (self.sise[0]-self.t,self.t))
				self.image.blit(self.image5, (self.t,self.sise[1]-self.t))
		else:
			self.image.fill((50,50,50))
			self.image.blit(self.l, (self.t+self.text_pos[0],self.t+self.text_pos[1]))




class WriteString():
	def __init__(self, pretext, sise, pos, lenght, funcTxt, mode="STR", color=WHITE, back=BLACK, active_color=GRAY100):
		self.pretext = unicode(pretext)
		self.type = "WS"
		self.sise = sise
		self.side = pos
		self.lenght = lenght
		self.color = color
		self.back = back
		self.active_color = active_color

		self.funcTxt = funcTxt
		self.func = False
		self.image = pygame.Surface((lenght, int(sise*1.2)))
		self.font = pygame.font.Font(_path+"/resources/FreeSansBold.ttf", int(sise*0.7))
		self.mode = mode

		self.string = ""
		self.active = False
		self.language_key = pretext
		self.shift = False

	def update(self, click, events):
		mpos = pygame.mouse.get_pos()
		if click:
			if mpos[0] > self.side[0] and mpos[0] < self.side[0]+self.lenght and mpos[1] > self.side[1] and mpos[1] < self.side[1]+self.sise*1.2:
				self.func = True
				self.active = _toogle(self.active)

		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LSHIFT:
					self.shift = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					self.shift = False				

		if self.active:
			for e in events:
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_RETURN:
						self.active = False
						self.func = True
					if e.key >= 97 and e.key < 256 and self.mode.upper() == "STR":
						if self.shift:
							self.string += chr(e.key).upper()
						else:
							self.string += chr(e.key)
					else:
						if e.key == 8:
							self.string = self.string[:-1]
#						print e.key
						if e.key in range(48,57):
							self.string += chr(e.key)

					if self.mode.upper() == "STR":
						if e.key == 32:
							self.string += "_"
			self.image.fill(self.active_color)
		else:
			self.image.fill(self.back)
		self.string_compiled = u"%s%s" % (self.pretext, self.string)
		self.image.blit(self.font.render(self.string_compiled, 0, self.color), (0,0))
