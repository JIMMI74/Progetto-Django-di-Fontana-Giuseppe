from django.views.generic.list import ListView
from forum.models import Section


class HomeView(ListView):
    queryset = Section.objects.all()
    template_name = "social_blog/homepage.html"
    context_object_name = "section_list"


