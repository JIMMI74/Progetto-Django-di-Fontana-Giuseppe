from django.urls import path
from .import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('newsection/', views.CreateSection.as_view(), name="create_section"),
    path("section/<int:pk>/", views.view_section, name="section_view"),
    path('section/<int:pk>/create_conversation', views.create_conversation, name="create_conversation"),
    path('conversation/<int:pk>/', views.conversation_view, name="view_conversation"),
    path('conversation/<int:pk>response/', views.response_conversation, name="response_conversation"),
    path('conversation/<int:id>/delete-post/<int:pk>/', views.DeletePost.as_view(), name="delete_post"),
    path("users/", views.UserList.as_view(), name="all_users_list"),
    path("user/<str:username>/", views.user_profile_view, name="user_profile"),
    path("forum/", include('forum.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
