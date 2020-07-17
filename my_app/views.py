from django.http import HttpResponse, HttpResponseRedirect #Redirect page
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'my_app/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username,password=password) #Autentic
    
    if user:
        django_login(request,user)
        #return HttpResponseRedirect('/home/') #Redirect pageHome
        return redirect('/home/')
    message = 'Credencias inválida'
    return render(request, 'my_app/login.html', {'message': message})
  
        
        
def home(request):
    return render(request, 'my_app/home.html')