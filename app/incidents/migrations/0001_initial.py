# Generated by Django 4.1.5 on 2023-02-20 18:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import incidents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('slug', models.SlugField(default='')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name_plural': 'Task Lists',
                'ordering': ['name'],
                'unique_together': {('group', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_created_by', to=settings.AUTH_USER_MODEL)),
                ('task_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='incidents.tasklist')),
            ],
            options={
                'ordering': ['priority', 'created_date'],
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('file', models.FileField(max_length=255, upload_to=incidents.models.get_attachment_upload_dir)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.task')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('email_from', models.CharField(blank=True, max_length=320, null=True)),
                ('email_message_id', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_comments', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.task')),
            ],
            options={
                'unique_together': {('task', 'email_message_id')},
            },
        ),
    ]
