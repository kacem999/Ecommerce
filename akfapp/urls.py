from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('purchase/', views.purchase, name="purchase"),
    path('checkout/', views.checkout, name="checkout"),
    path('category/<str:category>/', views.category, name='category'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
]
