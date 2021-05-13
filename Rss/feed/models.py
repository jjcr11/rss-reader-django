from django.db import models

class Page(models.Model):

    link = models.CharField(max_length=50)

class Post(models.Model):

    link = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    date_time = models.DateTimeField()
    authors = models.CharField(max_length=50)
    content = models.TextField()
    readed = models.BooleanField(default=False)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)