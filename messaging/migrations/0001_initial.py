# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 09:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.Keys')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('fromDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('toDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Whitelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.Keys')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whitelist', to='messaging.Message')),
            ],
        ),
        migrations.AddField(
            model_name='blacklist',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to='messaging.Message'),
        ),
    ]
