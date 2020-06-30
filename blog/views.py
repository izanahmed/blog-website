from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_post.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

#comment added for checking git
class PostDetailView(DetailView):
	model = Post

class LikeView(LoginRequiredMixin, View):
	login_url = ''
	redirect_field_name=''

	def post(self, *args, **kwargs):
		user = self.request.user
		pk = self.kwargs.get('pk')
		post_obj = Post.objects.get(id=pk)
	
		if user in post_obj.likes.all():
			post_obj.likes.remove(user)
		else:
			post_obj.likes.add(user)
			
		like, created = Like.objects.get_or_create(user=user,post_id=pk)
		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		like.save()
				
		return redirect(self.request.META.get('HTTP_REFERER'))




class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	success_message = "New post was created successfully!"
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	success_message = "Post updated successfully!"
	success_url = '/'
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_message = "Post deleted successfully!"
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		messages.warning(self.request, self.success_message)
		return super(PostDeleteView, self).delete(request, *args, **kwargs)


def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})


