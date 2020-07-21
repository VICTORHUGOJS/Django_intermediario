from django.http import HttpResponse, HttpResponseRedirect, HttpRequest #Redirect page
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import Address, STATES_CHOICES
# Create your views here.
def login(request : HttpRequest):
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
    return render(request, 'my_app/login.html', {'message': message}) #credencias invalida voltar pro login
  
@login_required(login_url='/login')        
def logout(request):
    django_logout(request)
    return redirect('/login/')
            
        
@login_required(login_url='/login')        
def home(request):
    return render(request, 'my_app/home.html')


@login_required(login_url='/login')
def address_list(request):
    addresses = Address.objects.all()  
    return render(request, 'my_app/address/list.html', {'addresses': addresses}) #Lista endereços

@login_required(login_url='/login')
def address_create(request):  #Cadastrar endereco form
     if request.method == 'GET':
        states = STATES_CHOICES
        return render(request, 'my_app/address/create.html', {'states': states})
    
     Address.objects.create(
        address=request.POST.get('address'),
        address_complement=request.POST.get('address_complement'),
        city=request.POST.get('address_complement'),
        state=request.POST.get('state'),
        country=request.POST.get('address_complement'),
        user=request.user
    )
     return redirect('/addresses/')