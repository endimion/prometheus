# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_submited', models.DateTimeField(verbose_name='date submitted')),
                ('pdf_file', models.FileField(upload_to='pdfs')),
                ('department_addressed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Department')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_class_name', models.CharField(max_length=100)),
                ('document_class_file', models.FileField(upload_to='tex')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.DocumentClass'),
        ),
    ]