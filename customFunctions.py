import datetime
import os

blog_directory = './blog'

def get_meta_data(path):
	# get path to meta data in post
	meta_data_path = os.path.join(path, "meta_data.txt")

	f = open(meta_data_path, 'r')
	content =  f.read().split('||')
	f.close()

	if len(content) == 3:
		content.append(None)

	return content

def build_blog_post_item(post):
	path = os.path.join(blog_directory, post)
	if os.path.isdir(path):
		title, date, visible, url = get_meta_data(path)

		if visible == 'true':
			if url == None:
				# remove the ./ in the path
				path = path[2:] + "/index.html"

				return date, "<font face='verdana'>" + \
					date + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
					 "<a target=\"_blank\" href=\"" + path + "\">" + title + "</a><br/>" + \
					 "</font>"
			else:
				return date, "<font face='verdana'>" + \
					date + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
					 "<a target=\"_blank\" href=\"" + url + "\">" + title + "</a><br/>" + \
					 "</font>"
		else:
			return date, ''
	else:
		print(path + " is not a directory and all is wrong.")
		return None, ""

def blogs():
	output_str = '<div class="container" name="blog">'
	output_str += '<div class="container">'

	items = os.listdir(blog_directory)

	dates   = []
	outputs = []

	for file_name in items:
		date, output= build_blog_post_item(file_name)

		if date == None or date == "" or output == "":
			continue

		dates.append(date)
		outputs.append(output)

	indexes = [i for i in range(len(dates))]
	indexes.sort(key=lambda x: datetime.datetime.strptime(dates[x], '%m/%d/%y'), reverse=True)

	for i in range(len(indexes)):
		output_str += outputs[indexes[i]]

	output_str += '</div>'
	output_str += '</div>'

	return output_str