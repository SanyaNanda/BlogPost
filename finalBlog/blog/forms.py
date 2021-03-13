from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField
from mptt.forms import TreeNodeChoiceField

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'author', 'body','tags')
		body = forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control', 'required':'false'}))

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the title of the blog here'}),
			'author':forms.TextInput(attrs={'class':'form-control','value':'', 'id':'sanya', 'type':'hidden'}),
			'tags':forms.TextInput(attrs={'class':'form-control','data-role':'tagsinput','name':'tags'}),
			#'body':forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control'})),
			#'author':forms.Select(attrs={'class':'form-control'}),
			#'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start writing your blog'}),
		}

class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'body')

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the title of the blog here'}),
			'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Start writing your blog'}),
			#'tags':forms.TextInput(attrs={'class':'form-control','data-role':'tagsinput'}),
		}

# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('comment', 'postSno')

# 		widgets = {
# 			'comments':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your comment'}),
# 			'postSno':forms.IntegerField(attrs={'class':'form-control','value':'{{ post.sno }}', 'type':'hidden'}),
# 		}

class NewCommentForm(forms.ModelForm):
	parent = TreeNodeChoiceField(queryset=Comment.objects.all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['parent'].widget.attrs.update({'class': 'd-none'})
		self.fields['parent'].label = ''
		self.fields['parent'].required = False

	class Meta:
		model = Comment
		fields = ('parent','comment')
		widgets = {
			'comment': forms.Textarea(attrs={'class': 'form-control'}),
	        }
	def save(self, *args, **kwargs):
		Comment.objects.rebuild()
		return super(NewCommentForm, self).save(*args, **kwargs)