from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import math


class Section(models.Model):
    name_section = models.CharField(max_length=80)
    description = models.CharField(max_length=150, blank=True, null=True)
    logo_section = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name_section

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def get_absolute_url(self):
        return reverse("section_view", kwargs={"pk": self.pk})

    def get_last_discussions(self):
        return Conversation.objects.filter(memebership=self).order_by("-create_date")[:2]

    def get_number_of_posts_in_section(self):
        return Post.objects.filter(conversation__membership=self).count()

class Conversation(models.Model):
    title = models.CharField(max_length=120)
    create_date = models.DateTimeField(auto_now_add=True)
    author_conversation = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    membership = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view_conversation", kwargs={"pk": self.pk})

    def get_n_pages(self):
        posts_conversation = self.post_set.count()
        n_page = math.ceil(posts_conversation / 5)
        return n_page

class Post(models.Model):
    author_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.author_post.username

