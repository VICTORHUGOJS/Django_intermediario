from django.http import HttpResponse, HttpResponseRedirect, HttpRequest #Redirect page
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import Address, STATES_CHOICES
from .forms import AddressForm
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
    addresses = Address.objects.all()  #cONSULTA TODOS REG NO BD
    return render(request, 'my_app/address/list.html', {'addresses': addresses}) #Lista endereços


@login_required(login_url='/login')
def address_create(request):                #Cadastrar endereco form
     if request.method == 'GET':
        #states = STATES_CHOICES
        form = AddressForm()                #Iniciando formulário
     else:
        form = AddressForm(request.POST)
        if form.is_valid():                    #Se for valido,  create
            Address.objects.create(             #Get mostrar o form Post cadastrar
                address=form.cleaned_data['address'],
                address_complement=form.cleaned_data['address_complement'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                user=request.user               #Relacionado o endereço com o usuario
            )
            return redirect('/addresses/')
        
        return render(request, 'my_app/address/create.html', {'form': form})
       
@login_required(login_url='/login')
def address_update(request,id):  #editar
     address = Address.objects.get(id=id)
     if request.method == 'GET':
        states = STATES_CHOICES
        return render(request, 'my_app/address/update.html', {'states': states, 'address': address})

     address.address=request.POST.get('address')
     address.address_complement=request.POST.get('address_complement')
     address.city=request.POST.get('city')
     address.state=request.POST.get('state')
     address.country=request.POST.get('country')
     #address.user=request.user #Relacionado o endereço com o usuario
     address.save()
  
     return redirect('/addresses/')