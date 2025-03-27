from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from posts.models import Post, Comment, Follow, Group, User
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from .pagination import CustomLimitOffsetPagination
from .permissions import AuthorOrReadOnly, ReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = CustomLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class CommentViewSet(viewsets.ViewSet):
    def get_queryset(self, post_id):
        # Возвращаем queryset комментариев, связанных с данным постом
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise(NotFound('Поста с таким id не существует'))
        return Comment.objects.filter(post=post)

    def list(self, request, post_id=None):
        queryset = self.get_queryset(post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, post_id=None):
        serializer = CommentSerializer(data=request.data)
        post = Post.objects.get(id=post_id)
        if serializer.is_valid() and request.user.is_authenticated:
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, post_id=None, comment_id=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, post_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise(NotFound('Комментария с таким id не существует'))

        serializer = CommentSerializer(comment,
                                       data=request.data, partial=True)
        if serializer.instance.author != request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, post_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise(NotFound('Комментария с таким id не существует'))

        serializer = CommentSerializer(comment,
                                       data=request.data, partial=True)
        if serializer.instance.author != request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id=None, comment_id=None):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise(NotFound('Комментария с таким id не существует'))

        serializer = CommentSerializer(comment,
                                       data=request.data, partial=True)
        if serializer.instance.author != request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        to_follow = self.request.data['following']
        try:
            user_to_follow = User.objects.get(username=to_follow)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # print(self.request.user, user_to_follow)
        if self.request.user == user_to_follow:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(self.request.user, user_to_follow)
        queryset = Follow.objects.filter(user=self.request.user)
        print(queryset)
        for elem in queryset:
            if elem.following == user_to_follow:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(user=self.request.user, following=user_to_follow)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)'''

class FollowViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
    
    def create(self, request):
        to_follow = self.request.data.get('following')
        try:
            user_to_follow = User.objects.get(username=to_follow)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if self.request.user == user_to_follow:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = FollowSerializer(data=request.data, context={'request': request})
        if serializer.is_valid() and request.user.is_authenticated:
            serializer.save(user=self.request.user, following=user_to_follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        queryset = self.get_queryset()
        search_terms = request.query_params.get('search', None)
        if search_terms:
            # Пример фильтрации по полям title и description
            queryset = queryset.filter(
                Q(following__username__icontains=search_terms))
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)
