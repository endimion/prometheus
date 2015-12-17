from django.shortcuts import render, redirect
from users.models import User
from .forms import LoginForm
from documents import views
from django.core.urlresolvers import reverse
import traceback

# Create your views here.


## todo clean up this view


def login(request):
    if not request.method == 'POST':
        loginForm = LoginForm()
        return render(request, 'login/the_login.html',{'form':loginForm})
    else:
        loginForm = LoginForm(request.POST)
        #loginForm.is_valid():
        if loginForm.is_valid():
            name = loginForm.cleaned_data['user_name']
            password = loginForm.cleaned_data['user_pass']
            try:
                user = User.objects.get(user_name=name)
                db_pass = user.user_password
                if(db_pass == password):
                    #print("Successfully logged in")
                    request.session['user_name'] = user.user_name
                    request.session['user_id'] = user.id
                    print (reverse('documents:wizard'))
                    return redirect(reverse('documents:wizard'))

                else:
                     # a message saying to try again to login should be displayed here
                     #print("User name password combination failed!")
                     error_message ="User name, password combination failed. Please try again" 
                     # clean the form
                     loginForm = LoginForm()
                     return render(request, 'login/the_login.html',{'form':loginForm, 'error_message':error_message})
            except Exception:
                traceback.print_exc()
                error_message ="User " + name +" not found!"
                loginForm = LoginForm()
                return render(request, 'login/the_login.html',{'form':loginForm, 'error_message':error_message}) 
                #print("User " + name  +" not found  ")
    return render(request, 'login/the_login.html',{'form':loginForm}) 

