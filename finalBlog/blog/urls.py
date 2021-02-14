from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('my_posts', views.MyPostView.as_view(), name="my_posts"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post_details"),
    path('add_post/',views.AddPostView.as_view(),name="add_post"),
    path('post/edit/<int:pk>',views.UpdatePostView.as_view(),name="update_post"),
    path('post/delete/<int:pk>',views.DeletePostView.as_view(),name="delete_post"),
    path('like/<int:pk>', views.LikeView, name='like_post'),
    path('liked_posts/', views.LikedView.as_view(), name='liked_posts'),
    path('post_comment/<int:pk>',views.postComment,name='post_comment')
]