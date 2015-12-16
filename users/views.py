from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from documents import views
#from urllib import urlencode
from django.core import serializers
import traceback
from django.core.urlresolvers import reverse
# Create your views here.

"""
demo view
"""
def index(request):
    return HttpResponse("this is a test view for the users")

"""
view for displaying a user by the user id
"""
def user_details(request,user_id):
    #message = "you are seeing the details for user %s"
    #return HttpResponse(message % user_id)
    user = get_object_or_404(User,pk=user_id) 
    return render(request,'users/user.html',{'user':user})


"""
view for registering a new user
"""
def register(request):
    if not request.method == 'POST':
        # return render(request,'users/register.html')
        theform = RegisterForm()
        return render(request,'users/register.html', {'form' : theform} )
    else:
        # generate a form from the request object
        form = RegisterForm(request.POST)
        #validate the form
        if form.is_valid():
            # process the form data
            name = form.cleaned_data['your_name']
            password = form.cleaned_data['your_password']
            date =  timezone.now()
            user = User(user_name=name,user_password=password,date_created=date)
            user.save()

        return render(request,'users/register.html',{'form':form})




"""
view for a user logging in the system
"""
def login(request):
    if not request.method == 'POST':
        loginForm = LoginForm()
        return render(request, 'users/login.html',{'form':loginForm})
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
                    print("Successfully logged in")
                    # here we should redirect to the appropriate page to generate the forms
                    # return redirect('documents.views.wizard', user=user) 
                    # return  HttpResponseRedirect(reverse('documents.views.wizard'), args=(),kwargs={'user':user})
                    #return redirect('documents.views.wizard',args=(user,))
                    #return render(request,'documents.views.wizard',{'user':user})
                    #serialized_user = serializers.serialize("json",[user,])
                    #request.session['user']= serialized_user

                    # the best way so far to do sessioncontrol for login stuff
                    # is to store in the session the user_name, and user_id
                    # after a user succesfully logs in 
                    request.session['user_name'] = user.user_name
                    request.session['user_id'] = user.id

                    return redirect(reverse('documents:wizard'))

                else:
                     # a message saying to try again to login should be displayed here
                     print("User name password combination failed!")
                     error_message ="User name, password combination failed. Please try again" 
                     # clean the form
                     loginForm = LoginForm()
                     return render(request, 'users/login.html',{'form':loginForm, 'error_message':error_message}) 
            except Exception:
                traceback.print_exc()
                error_message ="User " + name +" not found!"
                loginForm = LoginForm()
                return render(request, 'users/login.html',{'form':loginForm, 'error_message':error_message}) 
                #print("User " + name  +" not found  ")
    return render(request, 'users/login.html',{'form':loginForm}) 
