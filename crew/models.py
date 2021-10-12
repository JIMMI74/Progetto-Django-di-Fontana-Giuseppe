from django.db import models
from django.conf import settings
from django.utils import timezone
from .utils import sendTransaction
import hashlib
from django.urls import reverse


class RelatedPost(models.Model):
    name = models.CharField(max_length=122)
    surname = models.CharField(max_length=122, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=3000)
    published = models.DateTimeField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)


    def publish(self):
        self.published = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"

    def get_absolute_url(self):
        return reverse('post_detail.html', kwargs={"pk": self.pk})




class Post(models.Model):
    user = models.ForeignKey(RelatedPost, on_delete=models.CASCADE, related_name="post")
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=3000)
    slug = models.SlugField(max_length=250)
    datetime = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def publish(self):
        self.published = timezone.now()
        self.save()

    class Meta:
        verbose_name = "post received"
        verbose_name_plural = "posts received"

    def __str__(self):
        return self.title

    def write_On_Chain(self):
        self.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()





