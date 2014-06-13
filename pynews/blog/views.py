#from django.shortcuts import render
# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect  
import time
import hashlib
import re
from blog.models import News,User

# Create your views here.

'''首页'''		
def index(req,page=1):
	pagesize=10 #每页大小
	page=int(page)
	count=News.objects.all().count() #总记录数
	bloglist=News.objects.order_by("-createtime").all()[(page-1)*pagesize:page*pagesize] #latest blogs
	hotblog=News.objects.order_by('-viewcount')[0:10] #top 10

	if bloglist:
		for item in bloglist:
			item.createtime=timeFormat(item.createtime,True)#格式化日期
			item.content=trimHtmlTag(item.content)

	#计算页数
	pagecount=count/pagesize
	if count%pagesize!=0:
		pagecount+=1

	dataView={'hotblog':hotblog,'bloglist':bloglist}
	dataView['pagecount']=range(1,pagecount+1)
	dataView['page']=page #当前页码
	dataView['nav']=1 #导航焦点
	if 'userinfo' in req.session:
		dataView['userinfo']=req.session['userinfo'] #用户登入信息

	#print dataView
	return render_to_response('index.html',dataView,context_instance=RequestContext(req))

'''添加/编辑博客'''		
def new(req,id=0):
	#request logining
	if not CheckLogin(req):
		return HttpResponseRedirect('/login')

	userid=req.session['userinfo']['id']
	bloglist=News.objects.order_by('-createtime').filter(userid=userid)[0:5]
		
	if req.method=='GET':
		dataView={'showtip':False}
		

		#博客id［编辑加载］
		if id:
			req.session['login_from'] = req.META.get('HTTP_REFERER', '/')
			res=News.objects.filter(id=id)
			if res:
				res=res[0]
				if userid==res.userid: #判断该博客是否属于本用户
					dataView['title']=res.title
					dataView['content']=res.content
					dataView['id']=res.id
		
	else:
		msg=[]
		#表单验证
		if not req.POST.get('title',''):
			msg.append('标题不能为空')
		if not req.POST.get('content',''):
			msg.append('内容不能为空')

		if not msg:		
			#编辑博客
			if req.POST.get('id',''):
				q=News.objects.get(id=req.POST['id'])
				q.title=req.POST['title']
				q.content=req.POST['content']
				q.save()
				return HttpResponseRedirect(req.session['login_from'])
				
			else:
				#添加博客
				res=News.objects.create(title=req.POST['title'],content=req.POST['content'],author='',userid=req.POST['userid'],viewcount=0,createtime=time.time())
			
			dataView={'showtip':True, 'status':True,'msg':['操作成功']}
			
		else:
			dataView={'showtip':True,'status':False,'msg':msg,'title':req.POST.get('title',''),'content':req.POST.get('content','')}
		#res=News.objects.filter(id=2).update(title='fff')
	dataView['bloglist']=bloglist
	dataView['nav']=2
	if 'userinfo' in req.session:
		dataView['userinfo']=req.session['userinfo']

	return render_to_response('blog.new.html',dataView,context_instance=RequestContext(req))

'''显示博客'''		
def show(req,id):
	res=News.objects.filter(id=id)	
	if res:
		res=res[0]
		p=News.objects.get(id=id)
		if not p.viewcount:
			p.viewcount=0
		p.viewcount=p.viewcount+1
		p.save()

		res.createtime=timeFormat(res.createtime,True)
		if res.userid:
			u=User.objects.filter(id=res.userid)
			if u:
				res.author=u[0].username
			else:
				res.author=''
	dataView={'data':res}
	dataView['nav']=1
	if 'userinfo' in req.session:
		dataView['userinfo']=req.session['userinfo']

	return render_to_response('blog.detail.html',dataView,context_instance=RequestContext(req))

'''删除博客'''		
def delete(req,id):
	res=News.objects.filter(id=id)	
	if res:
		res=res[0]
		p=News.objects.get(id=id)		
		p.delete()

	return HttpResponseRedirect('/u/'+req.session['userinfo']['username'])

'''登入'''		
def login(req):
	if 'userinfo' in req.session and req.session['userinfo'] != None:
		return HttpResponseRedirect('/')

	if req.method=='GET':
		dataView={'showtip':False}
		req.session['login_from'] = req.META.get('HTTP_REFERER', '/')
	else:
		msg=[]
		if not req.POST.get('username',''):
			msg.append('请输入用户名')
		if not req.POST.get('password',''):
			msg.append('密码不能为空')

		if not msg:		
			res=User.objects.filter(username=req.POST['username'],password=hashlib.md5(req.POST['password']).hexdigest())
			if res:
				dataView={}
				res=res[0]
				userinfo={'id':res.id,'username':res.username}
				req.session['userinfo']=userinfo
				return HttpResponseRedirect(req.session['login_from'])
				#print res.username
			else:
				msg.append('用户名或密码错误')
				dataView={'showtip':True,'status':False,'msg':msg,'username':req.POST.get('username','')}
		else:
			dataView={'showtip':True,'status':False,'msg':msg,'username':req.POST.get('username',''),'password':req.POST.get('password','')}
	
	dataView['nav']=4
	if 'userinfo' in req.session:
		dataView['userinfo']=req.session['userinfo']

	return render_to_response('login.html',dataView,context_instance=RequestContext(req))

'''注册'''		
def regester(req):
	if 'userinfo' in req.session and req.session['userinfo'] != None:
		return HttpResponseRedirect('/')

	if req.method=='GET':
		dataView={'showtip':False}
		
	else:
		msg=[]
		status=False
		if not req.POST.get('username',''):
			msg.append('用户名不能为空')
		if not req.POST.get('password',''):
			msg.append('密码不能为空')
		if not req.POST.get('password2',''):
			msg.append('确认密码不能为空')

		if not msg:	
			if req.POST.get('password')!=req.POST.get('password2'):
				msg.append('两次输入密码不一致')
			if not msg:
				res=User.objects.filter(username=req.POST['username'])
				if res:
					msg.append('该用户名已经存在')
				else:
					#new user
					pwd=hashlib.md5(req.POST['password']).hexdigest()
					res=User.objects.create(username=req.POST['username'],password=pwd,truename=req.POST['username'],createtime=time.time())
					if res:
						status=True						
				
		dataView={'showtip':True,'status':status,'msg':msg,'username':req.POST['username'],'password':req.POST['password']}

	dataView['nav']=3
	if 'userinfo' in req.session:
		dataView['userinfo']=req.session['userinfo']

	return render_to_response('regester.html',dataView,context_instance=RequestContext(req))

'''个人主页'''
def home(req,username):
	res=User.objects.filter(username=username)
	dataView={}
	if res:
		#print res[0].id
		bloglist=News.objects.filter(userid=res[0].id) 
		if bloglist:
			for item in bloglist:
				item.createtime=timeFormat(item.createtime,True)#格式化日期
				item.content=trimHtmlTag(item.content)

		dataView['bloglist']=bloglist
		dataView['nav']=3
		dataView['userinfo']=req.session['userinfo']
		dataView['username']=username
		return render_to_response('home.html',dataView,context_instance=RequestContext(req))
	else:
		return HttpResponseRedirect('/')

'''判断是否登入'''
def loginout(req):
	if 'userinfo' in req.session :
		req.session['userinfo']=None
	return HttpResponseRedirect('/login')

'''判断是否登入'''
def CheckLogin(req):
	if 'userinfo' in req.session and req.session['userinfo'] != None:
		return True
	else:		
		return False

'''时间格式化'''
def timeFormat(t,isShort=False):
	timeArray = time.localtime(t)
	if  isShort:
		return time.strftime("%Y-%m-%d", timeArray)
	else:
		return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
 
'''过滤html标签'''
def trimHtmlTag(s):
	r=re.compile('</?\w+[^>]*>')	 
	if s:
		return r.sub('',s)
	return ""

