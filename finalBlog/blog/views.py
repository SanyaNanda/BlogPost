from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from blog.templatetags import extras

class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']
	#ordering = ['-id']

class MyPostView(ListView):
	model = Post
	template_name = 'my_posts.html'
	ordering = ['-post_date']

class PostDetailView(DetailView):
	model = Post
	template_name = 'post_details.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()

		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True

		comments=Comment.objects.filter(post=stuff, parent=None).order_by('-timestamp')
		replies=Comment.objects.filter(post=stuff).exclude(parent=None)
		replyDict={}
		for reply in replies:
			if reply.parent.sno not in replyDict.keys():
				replyDict[reply.parent.sno] = [reply]
			else:
				replyDict[reply.parent.sno].append(reply)
		
		context["total_likes"] = total_likes
		context["liked"] = liked
		context["comments"]=comments
		context["replyDict"]=replyDict
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

	def get_context_data(self, *args, **kwargs):
		context = super(UpdatePostView, self).get_context_data(**kwargs)
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		update_time = stuff.update()
		context['update_time'] = update_time


class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')

class LikedView(ListView):
	model = Post
	template_name = 'liked_posts.html'

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(LikedView, self).get_context_data(**kwargs)
	# 	stuff = get_object_or_404(Post)
	# 	liked='c'
	# 	if stuff.likes.filter(id=self.request.user.id).exists():
	# 		liked = self.request.user.id
	# 	context["liked"] = liked
	# 	return context

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


def postComment(request, pk):
	if request.method=="POST":
		comment = request.POST.get("comment")
		user = request.user
		postSno = request.POST.get("postSno")
		post = get_object_or_404(Post, id=request.POST.get('postSno'))
		parentSno = request.POST.get("parentSno")
		if parentSno == "":
			comment = Comment(comment=comment, user=user, post=post)
			comment.save()
			messages.success(request,"Your comment has been posted successfully!")
		else:
			parent = Comment.objects.get(sno = parentSno)
			comment = Comment(comment=comment, user=user, post=post, parent=parent)
			comment.save()
			messages.success(request,"Your Reply has been posted successfully!")
	return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))


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

		