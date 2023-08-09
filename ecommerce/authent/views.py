from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import generate_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def signup(request):

    if request.method == "POST":
        email = request.POST['email']
        passw = request.POST['pass1']
        conpassw = request.POST['pass2']
        if passw != conpassw:
            messages.warning(request, "Password does'nt match")
            # return HttpResponse('password incorrect')
            return render(request, 'signup.html')
        try:
            if User.objects.get(username = email):
                messages.warning(request, "Email Already Exists")
                # return HttpResponse('mail already exists')
                return render(request, 'authent/signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, passw)
        user.is_active=False
        user.save()
        # email sending for verifications
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        EMAIL_HOST_USER = 'balajisankar0202@gmail.com'
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        print(email_message.send())
        # send_mail() is not working
        # print(send_mail(
        #     email_subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     fail_silently=True,
        # ))

        print('mail sent successfully')
        messages.success(request, "Activate the link in your gmail")
        return redirect('/authent/login')
    return render(request, 'signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('/authent/login')
        return redirect(request, 'activatefail.html')




def handlelogin(request):

    if request.method == "POST":
        usernamee = request.POST["email"]
        upassword = request.POST["pass1"]
        myuser = authenticate(username=usernamee, password=upassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Successfully logined")
            return redirect('/')
        else:
            messages.warning(request, "Error in Login")
            return redirect('/authent/login/')
    return render(request, "login.html")

def handlelogout(request):
    logout(request)
    messages.success(request, 'Successfull Logged out')
    return render(request, 'login.html')



