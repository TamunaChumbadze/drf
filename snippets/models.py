# snippets/models.py
from django.db import models
from django.contrib.auth.models import User
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from django.utils import timezone

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.TextField()
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default="python",
        max_length=100
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default="friendly",
        max_length=100
    )
    linenos = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        related_name="snippets",
        on_delete=models.CASCADE
    )
    highlighted = models.TextField()
    is_public = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style,
            linenos=linenos,
            full=True,
            **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------- Comments --------
class Comment(models.Model):
    snippet = models.ForeignKey(
        Snippet, related_name="comments", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.owner.username}: {self.content[:20]}"


# -------- Likes --------
class Like(models.Model):
    snippet = models.ForeignKey(
        Snippet, related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('snippet', 'user')  # თითოეული user შეუძლია მხოლოდ ერთხელ like

    def __str__(self):
        return f"{self.user.username} likes {self.snippet.title}"