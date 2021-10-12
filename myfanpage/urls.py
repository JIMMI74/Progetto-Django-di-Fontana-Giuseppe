from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from crew.views import PostDetailView, RelatedPostListViewCBV, exercise, edenpoint, post_lasth, search
from social_blog.views import HomeView
from forum.views import contactPost, UserList
from django.conf import settings
from crew.views import RelatedCreateApiView, RelatedDetailAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', HomeView.as_view(), name='homepage'),
    path('message/<int:pk>/', PostDetailView.as_view(), name='post_detail.html'),
    path("list_users/", RelatedPostListViewCBV.as_view(), name='list_post.html'),
    path("contact/", contactPost, name='contact'),
    path('social_blog/', include('social_blog.urls')),
    path("users/", UserList.as_view(), name='all_users_list'),
    path("exercise/", exercise, name='some_exercise'),
    path("forum/", include('social_blog.urls')),
    path("account/", include('account.urls')),
    path("", include('social_blog.urls')),
    path('RelatedPost', edenpoint, name='eden_point_list'),
    path('postLastHour', post_lasth, name='postLastHour'),
    path("search/", search, name="search"),
    path("postserilizer/",  RelatedCreateApiView.as_view(), name="serializer"),
    path("allresialpost/", RelatedDetailAPIView.as_view(), name="post-detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
