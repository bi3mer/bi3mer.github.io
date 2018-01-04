# put in the #environment thing

from build_sites import build_templates, reimport
import time
import os

previous_counts = {}

def should_reset(path='.'):
	reset = False
	items = os.listdir(path)

	for file_name in items:
		file_name = os.path.join(path, file_name)

		if '.git' in file_name:
			continue
		elif os.path.isfile(file_name):
			file_modification_time = os.path.getmtime(file_name)

			if '.template.html'     in file_name or \
			   '.plugin.html'       in file_name or \
			   'customFunctions.py' in file_name:

				if file_name not in previous_counts:
					previous_counts[file_name] = file_modification_time
					reset = True
				else:
					if previous_counts[file_name] != file_modification_time:
						reset = True
						previous_counts[file_name] = file_modification_time
				
		elif os.path.isdir(file_name):
			reset = should_reset(path=file_name)

		if reset == True:
			return reset

	return reset

def main():
	os.popen("open index.html")

	should_reset()
	while True:
		time.sleep(1)

		if should_reset() == True:
			print "rebuilt"
			reimport()
			build_templates()

if __name__ == '__main__':
	main()
