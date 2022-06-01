
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .models import Commnt as ModelComment
from .form import CommentForm
from users.models import Profile
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import itertools




leaderbod_list = dict()
for user in User.objects.all():
	posts_by_user = Post.objects.filter(author = user)
	total_like_in_all_posts_of_user=0
	for i in posts_by_user:
		total_like_in_all_posts_of_user += i.number_of_likes()
	leaderbod_list[user.username]=total_like_in_all_posts_of_user
leaderbod_list = list(dict(sorted(leaderbod_list.items(), key=lambda item: item[1] ,reverse=True)).items())

def fun():

	leaderbod_list = dict()

	
	for user in User.objects.all():
		posts_by_user = Post.objects.filter(author = user)
		total_like_in_all_posts_of_user=0
		for i in posts_by_user:
			total_like_in_all_posts_of_user += i.number_of_likes()
		leaderbod_list[user.username]=total_like_in_all_posts_of_user
	leaderbod_list = dict(sorted(leaderbod_list.items(), key=lambda item: item[1] ,reverse=True))
	return list(leaderbod_list.items())

  	



	

# def home(request):
# 	context = {
# 		'posts': Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)



def PostLike(request, pk):
	global leaderbod_list
	
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	if post.likes.filter(id=request.user.id).exists():	
    	
		post.likes.remove(request.user)	
	else:

         post.likes.add(request.user)
	leaderbod_list = fun()
	 
	return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
	

	



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' 
	context_object_name = 'posts'	
	ordering = ['-date_posted']
	paginate_by = 4
	def  get_context_data(self, **kwargs):
		context = super(PostListView,self).get_context_data(**kwargs)
		posts = Post.objects.all()
		paginator = Paginator(posts, self.paginate_by)
		page = self.request.GET.get('page')
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		context["posts"] =posts 
		global leaderbod_list
		context["leaderbod_list"]=leaderbod_list
		
		return context

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' 

	ordering = ['-date_posted']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		posts = Post.objects.filter(author = user).order_by('-date_posted')
		global leaderbod_list
		context["leaderbod_list"]=leaderbod_list
		context['posts']=posts
		context['count']=posts.count()
		return context


class PostDetailView(DetailView):
	model = Post
	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		likes_connected = get_object_or_404(Post,id=self.kwargs['pk'])
		liked = False
		if likes_connected.likes.filter(id=self.request.user.id).exists():
			liked = True
		context['number_of_likes']=likes_connected.number_of_likes()
		context['post_is_liked']=liked


		#comment view logic
		pk = self.kwargs["pk"]
		
		form = CommentForm()
		post = get_object_or_404(Post, pk=pk)
		comments = post.comments.all()
		context['post'] = post
		context['posts']=Post.objects.all()
		context['comments'] = comments
		context['form'] = form
		global leaderbod_list
		context["leaderbod_list"]=leaderbod_list
		return context

	def post(self,request,*args, **kwargs):
		form = CommentForm(request.POST)
		self.object = self.get_object()
		context = super().get_context_data(**kwargs)
		post = Post.objects.filter(id=self.kwargs['pk'])[0]
		usr = Profile.objects.filter(user=request.user)[0]
		comments = post.comments.all()
		print(type(usr))
		image=usr
		
		context['post']=post
		context['comments']=comments
		
		context['form'] = form

		name = request.user
		if form.is_valid():
			content = form.cleaned_data['content']
	
		global leaderbod_list
		context["leaderbod_list"]=leaderbod_list
	

		comment=ModelComment.objects.create(name=name,content=content,post=post,img=image)
		form=CommentForm()

	
		return self.render_to_response(context=context)

	



class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'body','category']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'body','category']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})




