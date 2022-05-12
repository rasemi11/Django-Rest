from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import AppUserForm
from django.urls import reverse_lazy
from django.views import generic


class ProtectedView(TemplateView):
    template_name = 'base.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = AppUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
