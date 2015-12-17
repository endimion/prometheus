from django.conf.urls import url
from . import views


app_name='login'
urlpatterns = [
    #example /login/
    url(r'^$', views.login, name='login'),
    #url(r'^login/$',views.login, name = 'login2')

]



