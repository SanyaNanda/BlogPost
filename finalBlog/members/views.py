from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import SignUpForm, EditProfileForm, PassChangeForm, ProfilePageForm, EditProfilePageForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from blog.models import Profile, Post
# Create your views here.
class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	form_class = PassChangeForm
	template_name = 'registration/change_pass.html'
	success_url = reverse_lazy('password_changed')

def password_changed(request):
	return render(request, 'registration/pass_success.html')

class ShowProfilePageView(generic.DetailView):
	model = Profile
	template_name = 'registration/profile_page.html'

	def get_context_data(self, *args, **kwargs):
		users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		context["page_user"] = page_user
		return context 

class EditProfilePageView(generic.UpdateView):
	model = Profile
	template_name = 'registration/edit_profile_page.html'
	form_class = EditProfilePageForm
	#fields = ['bio', 'profile_pic', 'your_website', 'linkedin', 'twitter', 'fb', 'insta']
	success_url = reverse_lazy('home')

class CreateProfilePageView(generic.CreateView):
	model = Profile
	template_name = 'registration/create_profile_page.html'
	#Sfields = '__all__'
	form_class = ProfilePageForm

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
