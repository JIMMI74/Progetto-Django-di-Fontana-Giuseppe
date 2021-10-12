from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View


class StaffMixing(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
