from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView
from .forms import ConversationModelForm, PostModelForm, NewPostForm
from .mixins import StaffMixing
from .models import Conversation, Post, Section
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.contrib.admin.views.decorators import staff_member_required



def contactPost(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Post sent successfully!</h1")
    else:
        form = NewPostForm()
    context = {'form': form}
    return render(request, 'forum/contact.html', context)



class CreateSection(StaffMixing,CreateView):
    model = Section
    fields = "__all__"
    template_name = "forum/create_section.html"
    success_url = "/"


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = "forum/all_users_list.html"
    # context_object_name = "users_list"


def user_profile_view(request, username):           # Esercizo 2
    user = get_object_or_404(User, username=username)
    conversations_user = Conversation.objects.filter(author_conversation=user).order_by("-pk")
    context = {"user": user, "conversations_user": conversations_user}
    return render(request, 'forum/user_profile.html', context)

def view_section (request, pk):
    section = get_object_or_404(Section, pk=pk)
    conversations_section = Conversation.objects.filter(membership=section).order_by("-create_date")
    context = {"section": section, "conversations": conversations_section}
    return render(request, "forum/single_section.html", context)

@login_required
def create_conversation(request, pk):                  # ESERCIZIO 2
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        form = ConversationModelForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.membership = section
            conversation.author_conversation = request.user
            conversation.save()
            first_post = Post.objects.create(
                conversation=conversation,
                author_post=request.user,
                content=form.cleaned_data["content"],
            )
            return HttpResponseRedirect(conversation.get_absolute_url())
    else:
        form = ConversationModelForm()
    context = {"form": form, "section": section}
    return render(request, "forum/create_conversation.html", context)


def conversation_view(request, pk):                               # ESERCIZIO 2
    conversation = get_object_or_404(Conversation, pk=pk)
    posts_conversation = Post.objects.filter(conversation=conversation)
    paginator = Paginator(posts_conversation, 5)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    form_response = PostModelForm()
    context = {"conversation": conversation,
               "posts_conversation": posts,
               "form_response": form_response
               }
    return render(request, "forum/single_conversation.html", context)


@login_required
def response_conversation(request, pk):                         # ESERCIZIO 2
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.conversation = conversation
            form.instance.author_post = request.user
            form.save()
            url_conversation = reverse("view_conversation", kwargs={"pk": pk})
            page_in_conversation = conversation.get_n_pages()
            if page_in_conversation > 1:
                success_url = url_conversation + "?page=" + str(page_in_conversation)
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(url_conversation)

    else:
        return HttpResponseBadRequest()


#class AllPostListViewCBV(ListView):
#    model = Post
#    template_name = "forum/all_post_conversation.html"

class DeletePost(DeleteView):
    model = Post
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_post_id=self.request.user.id)


@staff_member_required
def ForumPostList(request, pk):                                             # ESERCIZIO 3
    conversation = get_object_or_404(Conversation, pk=pk)
    form_response = PostModelForm()
    posts_conversation = Post.objects.filter(conversation=conversation)
    context = {"conversation": conversation,
               "posts_conversation": posts_conversation,
               "form_response": form_response
               }
    return render(request, "forum/forum_post.html", context)





