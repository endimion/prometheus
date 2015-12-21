from django.db import models

# Create your models here.

USER_TYPE = ( ('admin', 'Administrator'), ('civil', 'Civilian'))



class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    date_created = models.DateTimeField('date created')
    user_type = models.CharField(max_length=5, choices=USER_TYPE, default='civil')


    def __str__(self):
        return self.user_name


