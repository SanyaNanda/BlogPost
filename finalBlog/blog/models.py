from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date
from django_ckeditor_5.fields import CKEditor5Field
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey 
from ckeditor.fields import RichTextField
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=255)
	header_image = models.ImageField(null=True, blank=True, upload_to="images/")
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	#body = models.TextField()
	#body = CKEditor5Field('Text', config_name='extends')
	body = CKEditor5Field('Text', config_name='extends', blank=True)
	post_date = models.DateTimeField(auto_now_add=True, editable=False)
	update_date = models.DateTimeField(blank=True, null=True)
	likes = models.ManyToManyField(User, related_name='blog_posts')
	saved = models.ManyToManyField(User, related_name='save_posts')
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
	#slug = models.SlugField(max_length=255, blank=True,null=True)
	tags = TaggableManager()

	def total_likes(self):
		return self.likes.count()

	def liked_by(self):
		return self.likes.all()

	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		#return reverse('post_details', args=(str(self.id)))
		return reverse('home')

	def update(self, *args, **kwargs):
		kwargs.update({'update_date': timezone.now})
		#super().update(*args, **kwargs)
		return self

# class Likes(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
# 	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')



class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField()
	profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile")
	your_website = models.CharField(max_length=255, null=True, blank=True)
	fb = models.CharField(max_length=255, null=True, blank=True)
	linkedin = models.CharField(max_length=255, null=True, blank=True)
	insta = models.CharField(max_length=255, null=True, blank=True)
	twitter = models.CharField(max_length=255, null=True, blank=True)
	
	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		#return reverse('post_details', args=(str(self.id)))
		return reverse('home')

class Comment(MPTTModel):
	#sno = models.AutoField(primary_key = True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parent_comment')
	comment = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	# publish = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=True)
	likes = models.ManyToManyField(User, related_name='commentlikes')

	class MPTTMeta:
		order_insertion_by = ['timestamp']

	def __str__(self):
		return self.comment[0:20] + '... by ' + str(self.user.username)

	def total_comments(self):
		return self.count()