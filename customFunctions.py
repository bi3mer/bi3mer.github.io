import os

blog_directory = './blog'

def build_blog_post_item(post):
	path = os.path.join(blog_directory, post)
	if os.path.isdir(path):
		return  path + " is directory"
	else:
		return path + " is not a directory and all is wrong."


def blogs():
	output_str = '<div class="container" id="blog">'
	output_str += '<div class="container">'
	output_str += '<ul>'

	items = os.listdir(blog_directory)

	for file_name in items:
		output_str += build_blog_post_item(file_name)

	output_str += '</ul>'
	output_str += '</div>'
	output_str += '</div>'

	return output_str