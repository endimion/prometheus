from django import forms
from .models import DocumentClass

class selectDocumentClassForm(forms.Form):
    document_class = forms.ModelChoiceField(queryset=DocumentClass.objects.all())

class createDocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentClass
        fields = ('document_fields',)


class newDocumentForm(forms.Form):
    def __init__(self,*args, **kwargs):
        doc_fields = kwargs.pop('doc_fields')
        super(newDocumentForm,self).__init__(*args,**kwargs)

        for df in doc_fields:
           #print( str(df) + " " + df )
           if df == "Κείμενο":
               self.fields['%s' %str(df)] = forms.CharField(label=str(df), widget=forms.Textarea)
           else:
               self.fields['%s' %str(df)] = forms.CharField(label=str(df))
