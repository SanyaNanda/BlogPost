from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'author', 'body')
		body = forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control'}))

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the title of the blog here'}),
			'author':forms.TextInput(attrs={'class':'form-control','value':'', 'id':'sanya', 'type':'hidden'}),
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
		}

# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('comment', 'postSno')

# 		widgets = {
# 			'comments':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your comment'}),
# 			'postSno':forms.IntegerField(attrs={'class':'form-control','value':'{{ post.sno }}', 'type':'hidden'}),
# 		}