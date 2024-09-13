from django.urls import path

from . import views

from cart.views import Cart
from .views import CustomLogoutView







app_name = 'my_app'


urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.LoginView.as_view(template_name='my_app/registrations/login.html'), name="login"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('my-account/', views.my_account, name="my_account"),
    path('my-account/edit/', views.edit_my_account, name="edit_account"),
    path('shop/', views.shop, name="shop"),


]