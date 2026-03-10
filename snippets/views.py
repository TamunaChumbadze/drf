# snippets/views.py
from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet, Comment, Like
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer, RegisterSerializer, CommentSerializer, LikeSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
            "comments": reverse("comment-list", request=request, format=format),
            "likes": reverse("like-list", request=request, format=format),
        }
    )


class SnippetList(generics.ListCreateAPIView):
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Snippet.objects.filter(is_public=True)
        tags = self.request.query_params.get("tags")
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)


# ---------------- Comments ----------------
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        snippet_id = self.kwargs.get("snippet_pk")
        return Comment.objects.filter(snippet_id=snippet_id)

    def perform_create(self, serializer):
        snippet_id = self.kwargs.get("snippet_pk")
        serializer.save(owner=self.request.user, snippet_id=snippet_id)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


# ---------------- Likes ----------------
class LikeList(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        snippet_id = self.kwargs.get("snippet_pk")
        return Like.objects.filter(snippet_id=snippet_id)

    def perform_create(self, serializer):
        snippet_id = self.kwargs.get("snippet_pk")
        serializer.save(user=self.request.user, snippet_id=snippet_id)


class LikeDetail(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


# ---------------- Users ----------------
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer