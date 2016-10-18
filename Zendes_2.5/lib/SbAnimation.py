class Animation():
	def __init__(self, sprites=None, time=100):
		self.sprites = sprites
		self.time = time
		self.work_time = 0
		self.skip_frame = 0
		self.frame = 0
	def update(self, dt):
		self.work_time += dt
		self.skip_frame = self.work_time / self.time
		if self.skip_frame > 0:
			self.work_time = self.work_time % self.time
			self.frame += self.skip_frame
			if self.frame >= len(self.sprites):
				self.frame = 0
	def get_sprite(self):
		return self.sprites[self.frame]


class LocAnimation():
	def __init__(self, keys={}):
		self.keys = keys
		self.frame = 2.0

	def __len__(self):
		return len(self.keys)

	def play(self, start=0.0, end=None, speed=1.0):
		pos = ()

		if end is None:
			end = max(self.keys)
		keyed0 = None
		keyed1 = None
		for key in self.keys:
			if key < int(self.frame):
				if keyed0 == None or key > keyed0:
					keyed0 = key
			if key > int(self.frame):
				if keyed1 == None or key < keyed1:
					keyed1 = key
		try:
			pos = self.keys[int(self.frame)]
		except KeyError:
			kd = False
			if keyed0 is None and keyed1 != None:
				pos = self.keys[keyed1]
				kd = True
			if keyed1 is None and keyed0 != None:
				pos = self.keys[keyed0]
				kd = True
			if not kd:
				if keyed0 is None and keyed1 is None:
					raise ValueError("animation keys list is empty")
				else:
					allsise = float(keyed1-keyed0)
					leftsise = float(self.frame-keyed0)
					rightsise = float(keyed1-self.frame)

					x0 = self.keys[keyed0][0]
					y0 = self.keys[keyed0][1]

					x1 = self.keys[keyed1][0]
					y1 = self.keys[keyed1][1]

					leftpercent = float(leftsise/allsise)
					rightpercent = float(rightsise/allsise)

					x = x0*leftpercent+x1*rightpercent
					y = y0*leftpercent+y1*rightpercent
					pos = (x,y)
		self.frame += speed
		if self.frame > end:
			self.frame = start
		return pos

			
			

#anim = LocAnimation({1:(1,2),25:(3,4),3:(5,6),24:(7,4)})
#anim = LocAnimation()
#while True:
#	position = anim.play()
#	print position
