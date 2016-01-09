from django.conf.urls import url
from . import views

app_name = "documents"
urlpatterns = [
    # example /documents/
    url(r'^$',views.wizard, name='wizard'),
    # example /documents/?field1 =value1&?field2=value2
    #url(r'^(?P<user>\w+?)/$',views.wizard),

    #example /documents/5/create
    url(r'^(?P<doc_id>[0-9]+)/create/$', views.create, name='create-document'),

    #example /documents/download
    url(r'^download/$', views.servePdf, name='servePdf'),

    #example /documents/upload
    url(r'^upload/$', views.getPdf, name='getPdf'),

]
