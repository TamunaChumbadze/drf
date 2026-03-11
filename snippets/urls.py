# snippets/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    # Registration
    path("register/", views.RegisterView.as_view(), name="register"),

    # ---------------- Web views ----------------
    path("", views.SnippetListView.as_view(), name="snippet-list-web"),           # Web snippet list
    path("<int:pk>/", views.SnippetDetailView.as_view(), name="snippet-detail-web"),  # Web snippet detail

    # ---------------- API views ----------------
    path("api/snippets/", views.SnippetList.as_view(), name="snippet-list"),
    path("api/snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"),
    path("api/snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),

    # Comments (nested under snippet)
    path("api/snippets/<int:snippet_pk>/comments/", views.CommentListCreate.as_view(), name="comment-list-create"),
    path("api/snippets/<int:snippet_pk>/comments/<int:pk>/", views.CommentDetail.as_view(), name="comment-detail"),

    # Likes (nested under snippet)
    path("api/snippets/<int:snippet_pk>/likes/", views.LikeList.as_view(), name="like-list"),
    path("api/snippets/<int:snippet_pk>/like/", views.ToggleLike.as_view(), name="toggle-like"),

    # Users
    path("api/users/", views.UserList.as_view(), name="user-list"),
    path("api/users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),

    # API root
    path("api/", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)