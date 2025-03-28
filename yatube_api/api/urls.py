from rest_framework import routers
# from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({
        'get': 'list', 'post': 'create'})),
    path('posts/<int:post_id>/comments/<int:comment_id>/',
         CommentViewSet.as_view({
             'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
             'patch': 'partial_update'})),
    path('follow/', FollowViewSet.as_view({'get': 'list', 'post': 'create'}))
]
