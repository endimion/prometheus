from django.conf.urls import url
from . import views

app_name='users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # example /users/12/
    url(r'^(?P<user_id>[0-9]+)+/$',views.user_details, name='user_details'),
    # example /users/register/
    url(r'^register/$',views.register,name='register'),

    #example /users/login
    url(r'^login/$',views.login, name = 'login')

]
