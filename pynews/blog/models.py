# coding=utf-8
from django.db import models

# Create your models here.
class News(models.Model):
	"""docstring for News"""
#	id=models.IntegerField()
	title=models.CharField(max_length=100)
	content=models.CharField(max_length=500)
	author=models.CharField(max_length=100)
	userid=models.IntegerField(null=True)
	viewcount=models.IntegerField(null=True)
	createtime=models.IntegerField(null=True)

	class Meta:
		db_table='test_news'
			

class User(models.Model):
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	truename=models.CharField(max_length=100)
	createtime=models.IntegerField(null=True)
	class Meta:
		db_table='common_user'

		
						