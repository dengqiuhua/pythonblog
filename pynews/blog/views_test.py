#from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader,Context
from django.shortcuts import render_to_response
import MySQLdb
import time
from django.db import connection
from blog.models import News

# Create your views here.
'''
def index(req):
	t=loader.get_template("blog.index.html")
	c=Context({})
	return HttpResponse(t.render(c))
'''

class BlogInfo(object):
	"""docstring for BlogInfo"""
	def __init__(self, title,content):
		self.blogTitle=title
		self.blogContent=content

	def show():
		pass
		
def index(req):
	user={'name':'monica','sex':'male'}
	#blog={'title':'blog-pynews','blogTitle':'this is my first blog','blogContent':'Hello ,monica.welcome to my python blog.'}
	bloglist=[]
	'''
	item=0
	while item<5:
		blog=BlogInfo('blog title'+str(item),'blogContent'+str(item))
		bloglist.append(blog)
		item+=1
	'''
	
	cur=connection.cursor()
	p1=News(title='django 2014',content='hello django.',author='monica',createtime=time.time())
	p1.save()
	#db
	db=MySQLdb.connect(user='root',db='testphp',passwd='',host='localhost')
	cursor=db.cursor()
	cursor.execute('SELECT id,title,content FROM test_news')
	for row in cursor.fetchall():
		#for newsinfo in row:	
			#print row		
			blog=BlogInfo(row[1],row[2])
			bloglist.append(blog)
	db.close()

	dataView={'user':user,'blog':blog,'bloglist':bloglist}
	return render_to_response('blog.index.html',dataView)