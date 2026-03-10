from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Snippet, Comment, Like


# ---------------- Snippets ----------------
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = (
            "url",
            "id",
            "highlight",
            "title",
            "description",
            "code",
            "linenos",
            "language",
            "style",
            "owner",
            "created",
            "updated",
            "is_public",
            "views",
            "tags",
        )


# ---------------- Comments ----------------
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = (
            "url",
            "id",
            "snippet",
            "owner",
            "content",
            "created",
        )


# ---------------- Likes ----------------
class LikeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = (
            "url",
            "id",
            "snippet",
            "user",
            "created",
        )


# ---------------- Users ----------------
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="snippet-detail",
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "snippets",
        )


# ---------------- Registration ----------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user