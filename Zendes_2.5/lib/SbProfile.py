import time

profiles = []

class Profiler():
	def __init__(self):
		self.points = {}
		self.lines = []
		self.startpoint = time.time()
		self.endpoint = None
		self.points["start"] = self.startpoint

	def add_point(self, key):
		self.points[key] = time.time()

	def add_line(self, key1, key2):
		self.lines.append((key1, key2))

	def end(self):
		self.endpoint = time.time()
		self.points["end"] = self.endpoint
		self.lines.append(("start", "end"))

	def get(self):
		print "profiling:\n"
		for line1 in self.lines:
			if line1 != ("start", "end"):
				print str(int(((self.points[line1[1]] - self.points[line1[0]])/(self.points["end"]-self.points["start"]))*100.0))+"%"+" %s" % (line1[1])

	def get_detal(self):
		for line1 in self.lines:
			if line1 != ("start", "end"):
				print str(self.points[line1[1]] - self.points[line1[0]])

def test():
	prof = Profiler()
	time.sleep(1)
	prof.add_point("new")
	prof.add_line("start", "new")
	time.sleep(1.5)
	prof.end()
	prof.get()
	print prof.lines
	print prof.points
