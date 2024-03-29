# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 09:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='info',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.Keys'),
        ),
        migrations.AddField(
            model_name='info',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL),
        ),
    ]
