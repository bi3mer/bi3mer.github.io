from time import strftime, gmtime
import os

directory_contents = os.listdir('.')

max_post_num = 0
for item in directory_contents:
	if os.path.isdir(item):
		num = int(item.split('_')[1])
		
		if num > max_post_num:
			max_post_num = num

path = 'post_' + str(max_post_num + 1)
os.mkdir(path)
os.mkdir(os.path.join(path, 'pictures'))

f = open(os.path.join(path, 'index.template.html'), 'w')
f.write("")
f.close()

f = open(os.path.join(path, 'meta_data.txt'), 'w')
f.write('Title' + ',' + strftime('%m/%d/%y', gmtime()))
f.close()
