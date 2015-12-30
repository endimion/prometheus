from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DocumentClass, Document, Department
from .forms import selectDocumentClassForm, createDocumentForm, newDocumentForm
from django.core.urlresolvers import reverse
import subprocess
import os
from django.utils import timezone
from users.models import User
from django.core.files import File

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
    departments = Department.objects.all()
    #

    if not request.method == 'POST':
        form  = newDocumentForm(None, doc_fields=document_form_fields, departments=departments)
        return render(request,'documents/newDocument.html',{'user_name':user_name, 'document_class': document_class, 'form':form, 'doc_id':doc_id, })
    else:
        form  = newDocumentForm(request.POST, doc_fields=document_form_fields, departments=departments)
        if form.is_valid():
            values_dic={}

            for dff in document_form_fields:
                values_dic[dff] = form.cleaned_data[dff]
                #print("the values passed by the form" + dff + " : " + values_dic[dff])

            template_path = document_class.document_class_file.path
            print( "the latex template is located at: " + template_path)

            # now we have to store the new pdf file with the appropriate metadata to the database
            date_submited = timezone.now()
            department_id = form.cleaned_data['department']
            dep_addressed = get_object_or_404(Department,id = department_id)
            values_dic['Τμήμα'] = dep_addressed.department_name

            # next we retrieve the documents already in the db. This is the protocol number
            document_count = len(Document.objects.all())
            print("there are  " + str(document_count) + " documents")

            # TODO fix so that the data is  inserted into the generated pdf document 
            generated_pdf_path = createPdf(template_path, str(document_count), values_dic)
            out_put_path = template_path


            # having generated the pdf file we can now upload it to the dbs

            # document_class  there already is a variable which contains the document class
            user_submitted= get_object_or_404(User, id= request.session.get('user_id'))
            doc_class = get_object_or_404(DocumentClass, document_class_name=document_class)

            doc = Document(date_submited=timezone.now(), document_class = doc_class,  user_submitted = user_submitted, pdf_file= generated_pdf_path, department_addressed = dep_addressed)
            doc.save()
            djangoFile = doc.pdf_file
 
            # print(djangoFile.path)
            # we add the generated file path to the session
            request.session['file_id'] = doc.id

        # return HttpResponse("so far so good")
        return render(request,'documents/fileCreated.html',{'file':djangoFile, })  




"""
this view is used to serve a pdf file for download to the user
"""
def servePdf(request):
    the_file = get_object_or_404(Document,id=request.session.get('file_id'))

    #print(file_id)
    filename = the_file.pdf_file.name.split('/')[-1]
    response = HttpResponse(the_file.pdf_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
#    return HttpResponse("so far so good")








"""
    simple method that copies a template tex file, builds the pdf and 
    then deletes the template
    @ returns the path to the generated pdf
"""
def createPdf(template_path, doc_id_number,values_dic):
    template_path_list = template_path.split(os.path.sep)
    # this will return smth like /home/nikos/PycharmProjects/prometheus/tex
    template_director = os.path.sep.join(template_path_list[:len(template_path_list)-1])
    # so we add another / here,
    template_director = template_director + os.path.sep
    temp_file_path = template_director+"temp"+doc_id_number+".tex"

    with open(template_path, "r") as inFile:
        with open(temp_file_path, "w") as outFile:
            for line in inFile:
                # we copy each line of the template file to the temp_file 
                # also adding the appropriate data if the line contains a key from the values_dic
                for key in values_dic:
                    if key in line:
                        if ':' in line:
                            line = line.replace(":", ": "+values_dic[key])
                        print(key + "--- " + line)

                outFile.write(line)
    # next we generate the pdf using xelatex
    p = subprocess.Popen(["xelatex", temp_file_path], cwd= template_director)
    p.wait()
    # clean up, i.e remove the .log, .aux, .tex generated files
    extensions = ['.log','.aux','.tex']
    for ext in extensions:
        p = subprocess.Popen(["rm", template_director+"temp"+doc_id_number+ext],cwd=template_director)
        p.wait()
    print("DASF" + temp_file_path)
    return template_director+"temp"+doc_id_number+".pdf"




