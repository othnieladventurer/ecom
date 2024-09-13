from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import View

from product.models import *
from product.views import *
from django.db.models import Q
from .forms import *


# Create your views here.


def index(request):
    product = Product.objects.all()[0:8]

    context = {
        'products':product,
    }
    return render(request, 'my_app/index.html',context)



class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('my_app:index')  # Redirect to the desired page after logout

    def get(self, request, *args, **kwargs):
        # Handle GET requests by redirecting to the home page or another view
        return self.post(request, *args, **kwargs)
    




def signup(request):
    if request.method == 'POST':
        form = SignupFormCreation(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect('/')
    else:
        form = SignupFormCreation()
        

    context = {
        'form': form
    }
    return render(request,'my_app/registrations/signup.html', context)


def login_(request):
    return render(request,'my_app/registrations/login.html')




def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')


    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {
        'products':products,
        'categories': categories,
        'active_category':active_category,
        'query': query
    }
    return render(request, 'my_app/shop.html', context)




@login_required
def my_account(request):
    return render(request, 'my_app/my_account.html')




@login_required
def edit_my_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        
        user.save()
        return redirect('my_app:my_account')
    
    return render(request, 'my_app/edit_my_account.html')