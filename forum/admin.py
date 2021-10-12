from django.contrib import admin
from .models import Conversation, Section, Post


# Register your models here.
class ConversationModelAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ["title", "membership", "author_conversation"]
    search_fields = ["title", " author_conversation"]
    list_filter = [" membership ", "create_date"]


class PostModelAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["author_post", "conversation"]
    search_fields = ["content"]
    list_filter = ["create_date", "author_post"]


class SectionModelAdmin(admin.ModelAdmin):
    model = Section
    list_display = ["name_section", "description"]


admin.site.register(Conversation)
admin.site.register(Section)
admin.site.register(Post)

