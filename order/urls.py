from django.urls import path

from . import views








app_name = 'order'


urlpatterns = [
    path('start_order/', views.start_order, name="start_order"),

]










