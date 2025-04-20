from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from myauth.models import Profile


class SetCookies(View):
    
    def get(self, request):
        response = HttpResponse('SetCookies')
        response.set_cookie('fizz', 'buzz', 120)
        return response


class GetCookies(View):

    def get(self, request: HttpRequest):
        value = request.COOKIES.get('fizz', 'default')
        return HttpResponse(value)


class SetSession(View):

    def get(self, request: HttpRequest):
        response = HttpResponse('SetCookies')
        request.session['example'] ='1234'
        return response


class GetSession(View):

    def get(self, request: HttpRequest):
        value = request.session.get('example', 'default')
        return HttpResponse(value)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'auth/register-view.html'
    success_url = reverse_lazy('shopapp:list_products')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        Profile.objects.create(user=user)
        login(request=self.request, user=user)
        return response
