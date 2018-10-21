# put in the #environment thing

from importlib import reload

import customFunctions
import inspect
import sys
import os

def reimport():
	try:
		reload(customFunctions) 
	except Exception as e:
		# print erro message and make beep to notify user of error
		print(e)
		sys.stdout.write('\r\a')

def build_template(file_name, path):
	f = open(file_name, 'r')

	output_file = file_name.replace('.template', '')
	output_str  = '<!-- auto-generated document -->\n'

	for line in f:
		if '{{' in line and '}}' in line:
			# remove brackets and ending new line to get file name
			file_name = os.path.join(path, line.split('{{')[1].replace('}}', '')[:-1])
			
			if os.path.isfile(file_name):
				file = open(file_name, 'r')
				output_str += file.read()
				file.close()
			else:
				file_name = file_name.split('.')[1].replace('/','')
				function = None
				for member in inspect.getmembers(customFunctions, inspect.isfunction): 
					if file_name in member[0]:
						function = member[1]
						break

				if function != None:
					output_str += function()	
				else:
					print(file_name + " is neither a vaid file nor a custom function.")
		else:
			output_str += line

	f.close()
	
	f = open(output_file,'w')
	f.write(output_str)
	f.close()

def build_templates(path='.'):
	items = os.listdir(path)

	for file_name in items:
		file_name = os.path.join(path, file_name)

		if '.git' in file_name:
			continue
		elif os.path.isfile(file_name):
			if '.template' in file_name:
				build_template(file_name, path)	
		elif os.path.isdir(file_name):
			build_templates(path=file_name)

if __name__ == '__main__':
 	build_templates() 