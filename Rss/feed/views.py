from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import feedparser
from feed.models import Page, Post
from datetime import datetime
from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.html_data = [
            {
                    "type": "",
                    "link": "",
                    "content": "",
                }
        ]
        self.current_link = ''
        self.current_type = ''
        #self.cont = 0

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.current_type = "link"
            self.current_link = dict(attrs)["href"]
        elif tag == "img":
            self.current_type = "image"
            self.current_link = dict(attrs)["src"]

    def handle_endtag(self, tag):
        if(tag == 'a'):
            self.html_data[-1]['type'] = self.current_type
            self.html_data[-1]['link'] = self.current_link
        if(tag == 'img'):
            self.html_data[-1]['type'] = self.current_type
            self.html_data[-1]['link'] = self.current_link
        if(tag == 'h1'):
            self.html_data[-1]['type'] = 'h1'
        if(tag == 'h2'):
            self.html_data[-1]['type'] = 'h2'
        if(tag == 'h3'):
            self.html_data[-1]['type'] = 'h3'
        if(tag == 'h4'):
            self.html_data[-1]['type'] = 'h4'
        if(tag == 'h5'):
            self.html_data[-1]['type'] = 'h5'
        if(tag == 'h6'):
            self.html_data[-1]['type'] = 'h6'
        #    if(self.html_data[-2]['type'] == 'text' and self.html_data[-2]['link'] == ''):
        #        self.html_data[-2]['content'] = self.html_data[-2]['content'] + self.html_data[-1]['content']
        #        self.html_data.pop()

    def handle_data(self, data):
        #content = ''
        #if data[0] == "\n":
        #data = data.replace("\n", "")
        self.html_data.append(
                {
                    "type": "text",
                    "link": "",
                    "content": data,
                }
            )

def index(request):
    feed = feedparser.parse("https://www.mientrastantoenmexico.mx/feed/")
    #feed = feedparser.parse("https://anthonyjyeung.medium.com/feed")
    print(feed.entries[0].published_parsed)
    print(feed.entries[0].published_parsed[0])
    nose2 = ""
    nose2 = nose2 + str(feed.entries[0].published_parsed[2]) + " "
    nose2 = nose2 + str(feed.entries[0].published_parsed[1]) + " "
    nose2 = nose2 + str(feed.entries[0].published_parsed[0]) + " "
    nose2 = nose2 + str(feed.entries[0].published_parsed[3]) + ":"
    nose2 = nose2 + str(feed.entries[0].published_parsed[4]) + ":"
    nose2 = nose2 + str(feed.entries[0].published_parsed[5])
    nose = datetime.strptime(nose2, '%d %m %Y %H:%M:%S')
    print(nose)
    return HttpResponse("dsadsd")

def feed(request):
    all_posts = []
    contador = 0
    posts = Post.objects.all()
    for post in posts:
        parser = MyHTMLParser()
        parser.feed(post.content)
        for cont in parser.html_data:
            p = re.compile(r'[\n ]')
            a = p.findall(cont['content'])
            if(len(a) == len(cont['content'])):
                cont['content'] = ''
        
        onePost = {
            'id': 0,
            'link': post.link,
            'title': post.title,
            'published': post.date_time,
            'authors': post.authors,
            'content': parser.html_data,
        }
        all_posts.append(onePost)

    all_post_sorted = sorted(all_posts, key=lambda item: item['published'])

    for post_sorted in all_post_sorted:
        post_sorted['id'] = contador
        contador = contador + 1

    return JsonResponse(all_post_sorted, safe=False)
    #return HttpResponse(all_post_sorted[-1])

def add_link(request, type, link):
    response  = {'status': 'Link added'}
    link2 = link.replace('^', '/')
    if type == 0:
        link2 = 'http://' + link2
    else:
        link2 = 'https://' + link2
    feed = feedparser.parse(link2)
    if(len(feed.entries) == 0):
        response['status'] = "ERROR"
    else:
        page = Page(link = link2)
        page.save()
    return JsonResponse(response)

def update_feed(request):
    pages = Page.objects.all()
    for page in pages:
        feed = feedparser.parse(page.link)
        for new in feed.entries:
            try:
                Post.objects.get_or_create(title = new.get("title",""))
            except:
                post = Post()
                if('link' in new):
                    post.link = new.link
                if('title' in new):
                    post.title = new.title
                if('published' in new):
                    dt = ""
                    dt = dt + str(new.published_parsed[2]) + " "
                    dt = dt + str(new.published_parsed[1]) + " "
                    dt = dt + str(new.published_parsed[0]) + " "
                    dt = dt + str(new.published_parsed[3]) + ":"
                    dt = dt + str(new.published_parsed[4]) + ":"
                    dt = dt + str(new.published_parsed[5])
                    post.date_time = datetime.strptime(dt, '%d %m %Y %H:%M:%S')
                if('authors' in new):
                    post.authors = new.authors
                if('content' in new):    
                    post.content = new.content[0]['value']
                else:
                    post.content = new.description




                post.page_id = page.id
                post.save()
    return JsonResponse({'status': 'You feed is updated'})

def mark_as_read(request, id):
    return HttpResponse(f"{id} marked as read")