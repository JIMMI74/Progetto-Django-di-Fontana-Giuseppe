from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Post, RelatedPost
from django.http import JsonResponse
from datetime import timedelta
import redis
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RelatedpostSerializer
from rest_framework.response import Response


def posts(requests):
    response = []
    posts = Post.objects.filter().order_by('datetime')
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'text': post.text,
                'user': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId

            }
        )

    return JsonResponse(response, safe=False)


def exercise(request):
    message = Post.objects.all()
    message_one = RelatedPost.objects.all()
    context = {"message": message, "message_one": message_one}
    return render(request, 'crew/exercise.html', context)


class PostDetailView(DetailView):               # ESERCIZIO 4
    model = RelatedPost
    template_name = "crew/post_detail.html"

    def post_detail(request):
        return render(request, 'crew/post_detail.html', {})


class RelatedPostListViewCBV(ListView):  # ESERCIZIO 4
    model = RelatedPost
    template_name = "crew/list_post.html"

def edenpoint(request):

    posts = RelatedPost.objects.filter(published__lte=timezone.now()).order_by('-published')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=None, decode_responses=True)
    client.lpush('ipList', ip)
    if client.lindex('ipList', 0) != client.lindex('ipList', 1):
        errMsg = 'Your IP address is different than before!'
    else:
        errMsg = ''
    return render(request, 'forum/eden_point_list.html', {'posts': posts, 'errMsg': errMsg})



def post_lasth(request):          # ESERCIZIO 5
    response = []
    this_hour = timezone.now()
    one_hour_before = this_hour - timedelta(hours=1)
    posts = RelatedPost.objects.filter(published__range=(one_hour_before, this_hour))
    for post in posts:
        response.append(
            {
                'title': post.title,
                'author': post.user.username,
                'datetime': post.created_date,
                'text': post.text
            }
        )
    if not response:
        return JsonResponse('No post has been published during the last hour', safe=False)
    return JsonResponse(response, safe=False)

# ESERCIZIO 6 N.B INUTILE CHE FACEVO cont String count= post.text.count(q) o sotto-forma di stringa
    # poichè con il queryset q inserito nel base.html,in search mi da ogni tipo di parola e stringa

def search(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        print(querystring)
        if len(querystring) == 0:
            return redirect("/search/")
        posts = RelatedPost.filter(contenuto__icontains=querystring)
        users = User.objects.filter(username__icontains=querystring)
        num_posts = posts.count()
        context = {"posts": posts, "users": users, "num_posts": num_posts}
        return render(request, 'crew/search.html', context)
    else:
        return render(request, 'crew/search.html')


class RelatedCreateApiView(APIView):

    def get(self,request):
        post = RelatedPost.objects.all()
        serializer = RelatedpostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RelatedpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RelatedDetailAPIView(APIView):
    def get_object(self, pk):
        post = get_object_or_404(RelatedPost, pk=pk)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = RelatedpostSerializer(post)
        return Response(serializer.data)

    def put(self,request, pk):
        post = self.get_object(pk)
        serializer = RelatedpostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status.HTTP_204_NO_CONTENT)





