from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from myauth.mixins import CanUpdateUserMixin
from myauth.models import Profile
from myauth.forms import UserForm, ProfileForm
from django.utils.decorators import method_decorator


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


class UserInfoView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'myauth/about-user.html'
    context_object_name = 'user_info'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return self.get_queryset().get(pk=pk)
        return self.request.user


class UsersListView(LoginRequiredMixin, ListView):
    queryset = Profile.objects.select_related('user')
    template_name = 'myauth/list-users.html'
    context_object_name = 'profiles'


class UserInfoUpdateView(LoginRequiredMixin, CanUpdateUserMixin, View):
    template_name = 'myauth/update-user-info.html'
    success_url = 'myauth/list-users.html'

    def get_object(self, pk):
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        return user, profile

    def get(self, pk, request):
        user, profile = self.get_object(pk)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        return render(request, self.template_name, context={
            'user_form': user_form,
            'profile_form': profile_form
        }
        )

    def post(self, request):
        user, profile = self.get_object()
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse(self.success_url))
        messages.error(request, "Введены неправильные данные!")
        return render(request, self.template_name, context={
            'user_form': user_form,
            'profile_form': profile_form
        }
        )












