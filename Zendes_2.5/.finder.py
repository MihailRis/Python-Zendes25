import os
import sys

def find(path, template):
	objects = os.listdir(path)
	for obj in objects:
		file_path = os.path.join(path, obj)
		if os.path.isfile(file_path):
			with open(file_path, 'r') as tfile:
				lines = tfile.readlines()
				for line in lines:
					if template in line:
						print ("\n\n\n%s\n%s\n%s\n" % (file_path,line.strip(),lines.index(line)))
		elif os.path.isdir(file_path):
			find(file_path, template)
					
				


if __name__ == "__main__":
	path = raw_input("Enter path: ")
	template = raw_input("Enter text: ")
	find(path, template)
