from django import forms
from .models import Conversation, Post
from django.forms import ModelForm
from crew.models import RelatedPost
from django.core.exceptions import ValidationError

class NewPostForm(ModelForm):       # ESERCIZIO 7
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "example@gmail.com"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "write here.."}))

    class Meta:
        model = RelatedPost
        fields = ["name", "surname", "email", "title", "text"]

    def clean_content(self):
        word = self.cleaned_data["text"]
        if "hack" in word:
            raise ValidationError("Word not Accept!!")


class ConversationModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "What do you think??"}),
        max_length=4000, label="Message")

    class Meta:
        model = Conversation
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title of Discussion"})
        }

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": "5"})}
        labels = {"content": "Message"}

