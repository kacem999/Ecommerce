from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup, name = "signup"),
    path('login/',views.handellogin, name = "login"),
    path('logout/',views.handleLogout, name = "logout"),
    path('activation/<uidb64>/<token>',views.ActivateAccounteViwe.as_view(),name='activation'),
    path('request-rest-email/',views.requestRestEmailView.as_view(),name='request-rest-email'),
    path('new-password/<uidb64>/<token>',views.SetNewPassword.as_view(),name='new-password'),
]