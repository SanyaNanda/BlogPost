from django.urls import path
from .views import HomeView, PostDetailView, AddPostView, UpdatePostView, DeletePostView, LikeView, LikedView, post_likes, MyPostView, MyLikedPostView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('my_posts', MyPostView.as_view(), name="my_posts"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post_details"),
    path('add_post/',AddPostView.as_view(),name="add_post"),
    path('post/edit/<int:pk>',UpdatePostView.as_view(),name="update_post"),
    path('post/delete/<int:pk>',DeletePostView.as_view(),name="delete_post"),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('liked_posts/', MyLikedPostView, name='liked_posts'),
]