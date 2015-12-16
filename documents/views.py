from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DocumentClass
from .forms import selectDocumentClassForm, createDocumentForm, newDocumentForm
from django.core.urlresolvers import reverse
import subprocess 



# Create your views here.


"""
view that corresponds to starting the new_document wizard
"""
def wizard(request):
    user_name = request.session.get('user_name')
    user_id   = request.session.get('user_id')
    #dropDown  =  DocumentClass.objects.all()
    form = selectDocumentClassForm()

    if not request.method=='POST':
        if user_name and user_id:
            print("got a user!", user_name, "with an id", user_id )
            return render(request,'documents/createDocument.html',{'user_name':user_name, 'form': form})
        else:
            print(" no user :( " )
    else:
        form = selectDocumentClassForm(request.POST)
        if form.is_valid():
            doc_class_name = form.cleaned_data['document_class']
            document_class = get_object_or_404(DocumentClass,document_class_name=doc_class_name)
            doc_id = document_class.id
            #render(request,'do
            #return create(request,doc_id)
            return redirect(reverse('documents:create-document',args=(doc_id,)))

    return HttpResponse('Hello, from the wizard!!')


"""
view to create a document from a given template, denoted by doc_id
"""
def create(request, doc_id):
    #return render(request,'t')
    user_name = request.session.get('user_name')
    document_class = get_object_or_404(DocumentClass,id=doc_id)
    document_form_fields = document_class.get_doc_fields()

    if not request.method == 'POST':
        form  = newDocumentForm(None, doc_fields=document_form_fields)
        return render(request,'documents/newDocument.html',{'user_name':user_name, 'document_class': document_class, 'form':form, 'doc_id':doc_id, })
    else:
        form  = newDocumentForm(request.POST, doc_fields=document_form_fields)
        if form.is_valid():
            values_dic={}

            for dff in document_form_fields:
                values_dic[dff] = form.cleaned_data[dff]
            #print(values_dic)
            # next we run the xelatex  process as a shell command
            print( "the latex template is located at: " + document_class.document_class_file.path)
            #call(["xelatex", document_class.document_class_file.path])
            p = subprocess.Popen(["xelatex", document_class.document_class_file.path], cwd= '/home/nikos/PycharmProjects/prometheus/tex/')
            p.wait()
        return HttpResponse("so far so good")

