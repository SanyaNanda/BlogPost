from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views
urlpatterns =[
	path('register/', UserRegisterView.as_view(),name='register'),
	path('edit_profile/', UserEditView.as_view(),name='edit_profile'),
	#path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_pass.html'),name='change_password'),
	path('change_password/', PasswordsChangeView.as_view(),name='change_password'),
	path('password_changed/', views.password_changed, name="password_changed"),
	path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='profile_page'),
	path('<int:pk>/edit_profile/', EditProfilePageView.as_view(), name='edit_profile_page'),
	path('create_profile/', CreateProfilePageView.as_view(), name='create_profile_page'),
]