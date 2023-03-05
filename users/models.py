from django.db import models
from django.conf import settings 
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    opportunity = models.CharField(max_length = 500)
    slug = models.SlugField(max_length=200,blank=True)
    created = models.DateField(auto_now=True)
    likes = models.ManyToManyField(User, related_name = 'posts')


    def total_likes (self):
        return self.likes.count

    # to ensure that the newest posts are at the top of the screen 
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return str(self.user)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super().save(*args,**kwargs)
    
class Comment (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
            return str(self.user.username)


