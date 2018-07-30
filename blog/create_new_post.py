from time import strftime, gmtime
import os

directory_contents = os.listdir('.')

path = 'post_RENAME_ME'
os.mkdir(path)
os.mkdir(os.path.join(path, 'pictures'))

f = open(os.path.join(path, 'index.template.html'), 'w')
f.write("")
f.close()

f = open(os.path.join(path, 'meta_data.txt'), 'w')
f.write('Title' + '||' + strftime('%m/%d/%y', gmtime()) + '||true')
f.close()
