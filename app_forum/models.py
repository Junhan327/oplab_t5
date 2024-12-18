from django.db import models
# Create your models here.
class user_info(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)


class article(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    tags = models.CharField(max_length=32)
    date = models.DateField(auto_now_add=True)
    likes = models.DecimalField(max_digits=6,decimal_places=0)
    author = models.ForeignKey(user_info,on_delete=models.CASCADE,null=True)
    collections = models.DecimalField(max_digits=6,decimal_places=0,default = 0)

class collection(models.Model):
    user = models.ForeignKey(user_info,on_delete=models.CASCADE)
    article =  models.ForeignKey(article,on_delete=models.CASCADE)

class img(models.Model):
    theimg = models.ImageField(upload_to='media')
    user = models.ForeignKey(user_info,on_delete=models.CASCADE,null=True)

class Comment(models.Model): 
    comment_article = models.ForeignKey(article,on_delete=models.CASCADE)
    comment_content = models.TextField()
    comment_author = models.ForeignKey(user_info,on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)