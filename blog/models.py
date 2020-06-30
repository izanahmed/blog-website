from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User,blank=True, default=None, related_name='post_likes')
	
	def __str__(self):
		return self.title

	def num_likes(self):
		return self.liked.all().count()
	def get_absolute_url(self, pk):
		return reverse('post-detail', kwargs=pk)

class Like(models.Model):
	Like_Choice=[('like', 'unlike')]
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	value = models.CharField(choices=Like_Choice,default='Like',max_length=20)

	def __str__(self):
		return str(self.post)
	