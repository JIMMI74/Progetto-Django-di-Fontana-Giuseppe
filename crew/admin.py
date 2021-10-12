from django.contrib import admin
# Register your models here.
from .models import Post, RelatedPost
admin.site.register(RelatedPost)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["id","user", "title", "user", "published"]
    list_filter = ["published", 'user']
    search_fields = ["title", "text"]

    class Meta:
        model = Post


class RelatedPost(admin.ModelAdmin):
    list_display = ["name", "surname", "email", "title", "datetime"]
    list_filter = ["published", 'user']
    search_fields = ["title", "text"]

    class Meta:
        model = RelatedPost


