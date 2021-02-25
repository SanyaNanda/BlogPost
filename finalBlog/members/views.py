from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm, EditProfileForm, PassChangeForm, ProfilePageForm, EditProfilePageForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from blog.models import Profile, Post
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')
	#success_url = reverse_lazy('create_profile_page')

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

class ShowProfilePageView(generic.TemplateView):
	model = Profile
	template_name = 'registration/profile_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		stuff = Post.objects.filter(author=page_user.user).order_by('-post_date')
		context["page_user"] = page_user
		context["stuff"] = stuff
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
	#success_url = reverse_lazy('login')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
            	if user.last_login is None:
            		login(request, user)
            		messages.info(request, f"You are now logged in as {username}")
            		return redirect('create_profile_page')
            	else:
            		login(request, user)
            		messages.info(request, f"You are now logged in as {username}")
            		return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "registration/login.html",
                    context={"form":form})
