from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# Email importens
from django.core.mail import EmailMessage
from django.conf import settings
from django.core import mail
# call TokenGenerator
from .utils import generateToken
# thread
import threading
#  password reset token generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


# Create your views here.
def signup(request):
    if request.method == "POST":
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')
        if get_password != get_confirm_password:
            messages.info(request, 'Password is not matching')
            return redirect('/auth/signup/')

        try:
            if User.objects.get(username=get_email):
                messages.warning(request, "Email is Taken")
                return redirect('/auth/signup/')
        except Exception as identifier:
            pass
        myuser = User.objects.create_user(get_email, get_email, get_password)
        myuser.is_active = False
        myuser.save()
        cureent_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('auth/activation.html', {
            'user': myuser,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),  # This generates safe URL
            'token': generateToken.make_token(myuser)  # the function in utils.py
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [get_email], )
        EmailThread(email_message).start()  # we use thread for quick deliver in case of many users
        messages.info(request, "Check Your Email")
        return redirect('login')

    return render(request, 'auth/signup.html')


# class based view
class ActivateAccounteViwe(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generateToken.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('login')
        return render(request, 'auth/activationFail.html')


@csrf_protect
def handellogin(request):
    if request.method == "POST":
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        myuser = authenticate(username=get_email, password=get_password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('index')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'auth/login.html')


def handleLogout(request):
    logout(request)
    messages.success(request, 'logout success')
    return render(request, 'auth/login.html')


class requestRestEmailView(View):
    def get(self, request):
        return render(request, 'auth/request-rest-email.html')

    def post(self, request):
        email = request.POST.get('email')
        myuser = User.objects.filter(email=email)
        if myuser.exists():
            cureent_site = get_current_site(request)
            email_subject = 'Reset Password'
            message = render_to_string('auth/request-user-email.html', {
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(myuser[0].pk)),  # why user[0] because maybe return list of users
                'token': generateToken.make_token(myuser[0]),
            })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,
                                         [email])  # the [] in 'to' because it can multiply receptors
            EmailThread(email_message).start()

            messages.info(request, "Check your email")

            return render(request, 'auth/request-rest-email.html')


class SetNewPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        try:
            if not generateToken.check_token(user, token):
                messages.warning(request, "IS Not Valid Url")
                return render(request,'auth/request-rest-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'auth/set-new-password.html',context)

    def post(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')
        if get_password != get_confirm_password:
            messages.info(request, 'Password is not matching')
            return render(request,'auth/set-new-password.html',context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(get_password)
            user.save()
            messages.success(request,"Change Password Succsfully")
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier :
            messages.error(request,"Something Went Wrong")
            return render(request,'auth/set-new-password.html',context)

        return render(request, 'auth/set-new-password.html', context)




