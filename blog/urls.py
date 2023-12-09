from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
            views.post_detail,
            name='post_detail'),
    path('tags/', views.TagListView.as_view(), name='tags_list'),
    path('tags/<str:tag>/', views.posts_by_tag, name='posts_by_tag'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/update', views.PostUpdateView.as_view(), name='post_update'),
]
