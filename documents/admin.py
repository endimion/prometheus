from django.contrib import admin
from .models import DocumentClass, Department, Document, DocumentFields

# Register your models here.
admin.site.register(DocumentClass)
admin.site.register(Department)
admin.site.register(Document)
admin.site.register(DocumentFields)
