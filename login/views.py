from django.shortcuts import render
from django.shortcuts import HttpResponse
from login import models
# Create your views here.
user_list = []

def index(request):
    # return HttpResponse("HELLO,WORD!")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username,password)
        # temp = {'user': username,'passwd' :password}
        # user_list.append(temp)
        models.UserInfo.objects.create(user=username, pwd=password)
    user_list = models.UserInfo.objects.all()
    return render(request,'index.html',{'data':user_list})