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

class collection(models.Model):
    user = models.ForeignKey(user_info,on_delete=models.CASCADE)
    article =  models.ForeignKey(article,on_delete=models.CASCADE)