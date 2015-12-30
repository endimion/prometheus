from django.db import models
from users.models import User

# Create your models here.
class DocumentFields(models.Model):
    document_field_name = models.CharField(max_length=30)

    def __str__(self):
        return self.document_field_name



class DocumentClass(models.Model):
    document_class_name = models.CharField(max_length=100)
    document_class_file = models.FileField(upload_to='tex')
    document_fields = models.ManyToManyField(DocumentFields)

    def __str__(self):
        return self.document_class_name
    # this method returns as a vector all the document_fields of the object
    def get_doc_fields(self):
        res = []
        for df in self.document_fields.all():
           #print(str(df))
           res.append(str(df))
        return res




class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class Document(models.Model):
    date_submited = models.DateTimeField('date submitted')
    department_addressed = models.ForeignKey(Department, on_delete=models.CASCADE)
    document_class = models.ForeignKey(DocumentClass, on_delete=models.CASCADE)
    user_submitted = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs')


    def __str__(self):
        return self.user_submitted.user_name + "_" + str(self.id) + "_" 

