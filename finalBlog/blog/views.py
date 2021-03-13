from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, edit
from .models import Post, Comment
from .forms import PostForm, EditForm, NewCommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from blog.templatetags import extras
from django.utils import timezone
from hitcount.views import HitCountDetailView
from django.db.models import Q


class TagMixin(object):
	def get_context_data(self,**kwargs):
		context = super(TagMixin, self).get_context_data(**kwargs)
		context['tags'] = Post.tags.all()
		return context

class HomeView(TagMixin, ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']
	#ordering = ['-id']

	# def get_context_data(self, **kwargs):
	# 	context = super(HomeView, self).get_context_data(**kwargs)
	# 	context.update({
	# 		'popular_posts': Post.objects.order_by('-hit_count_generic')[:3],
	# 		})
	# 	return context

class TagIndexView(TagMixin, ListView):
	template_name = 'home.html'
	model = Post

	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

class MyPostView(ListView):
	model = Post
	template_name = 'my_posts.html'
	ordering = ['-post_date']

class PostDetailView(edit.FormMixin, HitCountDetailView):
	model = Post
	template_name = 'post_details.html'
	context_object_name = 'post'
	count_hit = True
	form_class = NewCommentForm


	def post(self, *args, **kwargs):
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		comments = Comment.objects.filter(post=stuff, status=True)
		user_comment = None

		if self.request.method == 'POST':
			comment_form = self.get_form()
			if comment_form.is_valid():
				user_comment = comment_form.save(commit=False)
				user_comment.post = stuff
				user_comment.user = self.request.user
				user_comment.save()
				return HttpResponseRedirect(self.request.path_info)
		else:
			comment_form = self.get_form()
		return HttpResponseRedirect(self.request.path_info)


	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()

		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True

		saved = False
		if stuff.saved.filter(id=self.request.user.id).exists():
			saved = True

		comments = Comment.objects.filter(post=stuff, status=True)	
		context["total_likes"] = total_likes
		context["liked"] = liked
		context["saved"] = saved
		context["comments"] = comments
		context["comment_form"] = self.get_form()
		return context

class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'

class UpdatePostView(UpdateView):
	model = Post
	form_class = EditForm
	template_name = 'update_post.html'

	def get_object(self):
		obj = super().get_object()
		# Record the last accessed date
		obj.update_date = timezone.now()
		obj.save()
		return obj

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(UpdatePostView, self).get_context_data(**kwargs)
	# 	stuff = get_object_or_404(Post, id=self.kwargs['pk'])
	# 	update_time = stuff.update()
	# 	context['update_time'] = update_time


class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

class LikedView(ListView):
	model = Post
	template_name = 'liked_posts.html'

class SavedView(ListView):
	model = Post
	template_name = 'saved_posts.html'

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(LikedView, self).get_context_data(**kwargs)
	# 	stuff = get_object_or_404(Post)
	# 	liked='c'
	# 	if stuff.likes.filter(id=self.request.user.id).exists():
	# 		liked = self.request.user.id
	# 	context["liked"] = liked
	# 	return context

def CommentLikeView(request, pk):
	comment = get_object_or_404(Comment, id=request.POST.get('commentt_id'))
	liked = False
	if comment.likes.filter(id=request.user.id).exists():
		comment.likes.remove(request.user)
		liked = False
	else:
		comment.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('post_details', args=[str(comment.post.id)]))

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))

def SaveView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	saved = False
	if post.saved.filter(id=request.user.id).exists():
		post.saved.remove(request.user)
		saved = False
	else:
		post.saved.add(request.user)
		saved = True
	return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))


# def postComment(request, pk):
# 	# if request.method=="POST":
# 	# 	comment = request.POST.get("comment")
# 	# 	user = request.user
# 	# 	postSno = request.POST.get("postSno")
# 	# 	post = get_object_or_404(Post, id=request.POST.get('postSno'))
# 	# 	parentSno = request.POST.get("parentSno")
# 	# 	if parentSno == None:
# 	# 		comment = Comment(comment=comment, user=user, post=post)
# 	# 		comment.save()
# 	# 		messages.success(request,"Your comment has been posted successfully!")
# 	# 	else:
# 	# 		parent = Comment.objects.get(sno = parentSno)
# 	# 		comment = Comment(comment=comment, user=user, post=post, parent=parent)
# 	# 		comment.save()
# 	# 		messages.success(request,"Your Reply has been posted successfully!")
# 	# return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))
# 	post = get_object_or_404(Post, id=request.POST.get('post_id'))
# 	comments = Comment.objects.filter(post=post, status=True)
# 	user_comment = None

# 	if request.method == 'POST':
# 		comment_form = NewCommentForm(request.POST)
# 		if comment_form.is_valid():
# 			user_comment = comment_form.save(commit=False)
# 			user_comment.post = post
# 			user_comment.save()
# 			return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))
# 	else:
# 		comment_form = NewCommentForm()
# 	return render(request, 'post_details.html', {'post': post, 'comments':  user_comment, 'comments': comments, 'comment_form': comment_form})

def search(request):
	querys = request.GET.get('query').split()
	query = Q()
	for word in querys:
		query = query | Q(title__icontains=word) | Q(author__first_name__icontains=word) | Q(author__last_name__icontains=word) | Q(author__username__icontains=word) | Q(body__icontains=word) | Q(tags__name__icontains=word)
	results = Post.objects.filter(query).distinct()
	params = {'allPost': results}
	return render(request, 'search.html', params)
	# titles = Post.objects.filter(title__icontains=query)
	#tags = Post.objects.filter(tags__icontains=query)
	# first = Post.objects.filter(author__first_name__icontains=query)
	# last = Post.objects.filter(author__last_name__icontains=query)
	# username = Post.objects.filter(author__username__icontains=query)
	# body = Post.objects.filter(body__icontains=query)
	# search = titles.union(body,first,last,username)
	
	#return HttpResponse('This is search')
# def MyLikedPostView(request):
# 	post = get_object_or_404(Post)
# 	context={}
# 	l=[]
# 	for i in post:
# 		if i.likes.filter(id=request.user.id).exists():
# 			l.append(request.user.username)
# 	context['post_liked'] = l
# 	return render(request, 'liked_posts.html', context)


# def LikedView(request, pk):
# 	post = get_object_or_404(Post, id=request.POST.get('post_id'))
# 	l=[]
# 	if post.likes.filter(id=request.user.id).exists():
# 		l.append(post)
		
# 	return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))


# class LikedView(ListView):
# 	model = Post
# 	template_name = 'liked_posts.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(LikedView, self).get_context_data(**kwargs)
# 		l=[]
# 		for i in get_object_or_404(Post).likes.filter(id=self.request.user.id):
# 			l.append(i)
		

# 		context["posts"] = l
# 		return context

# def post_likes(request, pk):
#     posts = Post.objects.all()
#     post_likes = posts.likes.all()
#     context = {'post_likes': post_likes,}
#     return render(request, 'liked_posts.html', context)

		