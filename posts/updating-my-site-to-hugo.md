+++
date = '2024-11-23T12:00:19-05:00'
draft = false
title = 'Updating My Site to Hugo'
+++
It's been over two years since I last made a post, and a lot has happened. One of the most minor of these is the change to my website: I'm now using [Hugo](https://gohugo.io/) to build the whole thing.

Before Hugo, I was using a [home-brewed tool I built in Python](https://github.com/bi3mer/bi3mer.github.io/blob/cbeee3a33913750b004cefade52fa29f529dd3d4/build_sites.py). It worked with [HTML](https://en.wikipedia.org/wiki/HTML), but there were re-writable portions marked by `{{ FILE_LOCATION }}`. The tool would go to that file location and replace the line with whatever it found in that file. I also had a blog post system with a meta file with information like the title and the data of the blog post, and more features. However, it was a pain to work with.

The problem was the direct use of HTML. Every blog post I wrote had to be written directly in HTML. So, when I wanted to add a link, I was going through the motions of `<a href="...">...</a>`, and that became more and more cumbersome. If I didn't write directly in an HTML text file, I wrote the post in [Google Docs](https://docs.google.com/), and then I converted it to HTML after the fact. Either way, there was extra work, which made me want to avoid writing about what I was working on. 

This is why I wanted to make a change, but why Hugo? I didn't need to use it. I could have used something like [Python-Markdown](https://python-markdown.github.io/reference/) to convert [Markdown](https://en.wikipedia.org/wiki/Markdown) to HTML. With it, I could've added another field to the meta file format to mark that a Markdown file should be used. But I didn't.

I wish that I could tell you I really put a lot of thought into using Hugo instead of a tool like [Jekyll](https://jekyllrb.com/), but nope. I saw a [Fireship YouTube video](https://www.youtube.com/watch?v=0RKpf3rK57I&t) about Hugo and decided to try it out. Trying it out went well enough, so I converted my entire site.

It could have been a smoother process at the start. I wanted to make my own custom [theme](https://themes.gohugo.io/) at the beginning so that the website would be more representative of me and what I am capable of, but I quickly came to the conclusion that I was wrong. The themes in Hugo have gone through a ton of work. The one I'm using, [PaperMod](https://github.com/adityatelange/hugo-PaperMod), has over 1,100 commits. I'm not willing to put that much work into this website, so using a theme was the decision for me. Once I had a theme, everything became a lot easier. 

Still, there were some rough edges. Probably the most work went into the home page. The default home page for PaperMod has a list of posts, but I didn't want that. This led me to learn that you can overwrite themes with a `layout` directory of your own. You can also write [shortcodes](https://gohugo.io/content-management/shortcodes/) in that directory, which lets you put HTML into Markdown files with arguments. Once I figured that out, everything became a lot easier. 

After that, I had to convert all of my blog post posts from HTML to MarkDown. It was a time-consuming and, frankly, boring process, but it is one that is finally done. I ended up getting rid of some of the ones that I didn't like in the process---however, they can still be found in the [commit history of the GitHub repository](https://github.com/bi3mer/bi3mer.github.io/commits/master/). 

Regardless, the important part is that the process is complete, and I feel like I want to write about the stuff I have done. Seems like a success to me. I'm particularly proud of the game's page. I think it is a huge improvement on my previous iteration. 