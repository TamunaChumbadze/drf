# snippets/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    # Registration
    path("register/", views.RegisterView.as_view(), name="register"),

    # Snippets
    path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
    path("snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"),
    path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),

    # Comments (nested under snippet)
    path("snippets/<int:snippet_pk>/comments/", views.CommentList.as_view(), name="comment-list"),
    path("snippets/<int:snippet_pk>/comments/<int:pk>/", views.CommentDetail.as_view(), name="comment-detail"),

    # Likes (nested under snippet)
    path("snippets/<int:snippet_pk>/likes/", views.LikeList.as_view(), name="like-list"),
    path("snippets/<int:snippet_pk>/likes/<int:pk>/", views.LikeDetail.as_view(), name="like-detail"),

    # Users
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),

    # API root
    path("", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)