from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.models import Profile
class Post(models.Model):
    CHOICES = (
    	("Andriod", "Andriod"),
    	("iOS", "iOS"),
    	("Web", "Web"),
    	("Windows", "Windows"),
					)
    likes =   models.ManyToManyField(User, related_name='like')
    title = models.CharField(max_length = 100)



    body = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.CharField(max_length=100,choices = CHOICES,
        default = 'Software')
    
    def get_absolute_url(self):
	    return reverse('post-detail', kwargs = {'pk': self.pk})

    def number_of_likes(self):
        return self.likes.count()

    def number_of_comments(self):
        return self.comments.all().count()

    class Meta:
        ordering = ['-date_posted']  






def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

class Commnt(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(default = timezone.now)

    name =models.ForeignKey(User, on_delete = models.CASCADE,related_name='commented_user')
    img=models.ForeignKey(Profile, on_delete = models.CASCADE,related_name='commented_user_img')
    objects = models.Manager()
  

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return '{}'.format(self.content)
