from django.shortcuts import render, HttpResponse, redirect
from wbsapp.models.indexModel import Person
from wbsapp.views.indexView import project
from django.template import Context, Template
import datetime, sys

# Create your views here.
def login(request):
    context = {}

    userid = request.POST.get('userid')
    if userid:
        context['userid'] = userid
        try:
            personInfo = Person.objects.get(personID=userid)
            if personInfo:
                password = request.POST.get('password')
                # if make_password(password)==person.password:
                if password == personInfo.password:
                    # context['personID'] = personInfo.personID
                    request.session['userid'] = userid
                    request.session['username'] = personInfo.personName
                    return redirect(to='project')
                else:
                    context['errPassword'] = '入力したパスワードが存在しません。'
        except ValueError:
            context['loginErr'] = 'ユーザーIDの形式が正しくありません。'
        except:
            context['loginErr'] = '入力したユーザーIDが存在しません。'

    index_page = render(request, 'login.html', context)
    return index_page


# Create your views here.
def logout(request):
    request.session.clear()
    return redirect(to='login')
