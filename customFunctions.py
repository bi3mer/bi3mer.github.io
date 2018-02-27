import os

blog_directory = './blog'

def get_meta_data(path):
	# get path to meta data in post
	meta_data_path = os.path.join(path, "meta_data.txt")

	f = open(meta_data_path, 'r')
	return f.read().split('||')

def build_blog_post_item(post):
	path = os.path.join(blog_directory, post)
	if os.path.isdir(path):
		title, date, visible = get_meta_data(path)

		if visible == 'true':
			# remove the ./ in the path
			path = path[2:] + "/index.html"

			return  date + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "<a target=\"_blank\" href=\"" + path + "\">" + title + "</a><br/>"
		else:
			return ''
	else:
		print path + " is not a directory and all is wrong."
		return ""

def blogs():
	output_str = '<div class="container" name="blog">'
	output_str += '<div class="container">'
	output_str += '<ul>'

	items = os.listdir(blog_directory)

	for file_name in items:
		output_str += build_blog_post_item(file_name)

	output_str += '</ul>'
	output_str += '</div>'
	output_str += '</div>'

	return output_str