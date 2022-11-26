# from pickle import _BufferCallback
from django.db import models
from django.conf import settings 
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'images/%y/%m/%d')
    caption = models.TextField(blank=True)
    title = models.CharField(max_length = 500)
    slug = models.SlugField(max_length=200,blank=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
