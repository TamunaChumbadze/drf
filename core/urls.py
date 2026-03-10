# snippets/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),

    # Snippets
    path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
    path("snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"),
    path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),

    # Comments
    path("snippets/<int:snippet_pk>/comments/", views.CommentListCreate.as_view(), name="comment-list-create"),

    # Likes
    path("snippets/<int:snippet_pk>/likes/", views.LikeList.as_view(), name="like-list"),
    path("snippets/<int:snippet_pk>/like/", views.ToggleLike.as_view(), name="toggle-like"),

    # Users
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),

    # API root
    path("", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)