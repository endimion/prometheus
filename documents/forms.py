from django import forms
from .models import DocumentClass, Department


class selectDocumentClassForm(forms.Form):
    document_class = forms.ModelChoiceField(queryset=DocumentClass.objects.all())

class createDocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentClass
        fields = ('document_fields',)


class newDocumentForm(forms.Form):
    #my_field = forms.CharField(max_length=30)

    def __init__(self,*args, **kwargs):
        doc_fields = kwargs.pop('doc_fields')
        departs_db = kwargs.pop('departments')

        depart_choices = []
        depart_id = []
        for dep in departs_db:
            depart_choices.append(dep.department_name)
            depart_id.append(dep.id)

        CHOICES = tuple(zip(depart_id,depart_choices))

        super(newDocumentForm,self).__init__(*args,**kwargs)

        for df in doc_fields:
           if df == "Κείμενο":
               self.fields['%s' %str(df)] = forms.CharField(label=str(df), widget=forms.Textarea)
           else:
               if not df == "ΠΡΟΣ":
                   self.fields['%s' %str(df)] = forms.CharField(label=str(df))

        self.fields['department'] = forms.ChoiceField(choices=CHOICES,label='Τμήμα')



class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
