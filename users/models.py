from django.db import models

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    date_created = models.DateTimeField('date created')

    def __str__(self):
        return self.user_name


