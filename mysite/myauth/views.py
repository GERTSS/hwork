from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse
from django.views import View


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
