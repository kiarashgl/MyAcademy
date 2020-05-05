# Generated by Django 3.0.5 on 2020-05-05 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='score',
        ),
        migrations.RemoveField(
            model_name='department',
            name='university_name',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='department_name',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='score',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='university_name',
        ),
        migrations.AddField(
            model_name='department',
            name='my_university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.University'),
        ),
        migrations.AddField(
            model_name='entity',
            name='picture',
            field=models.ImageField(null=True, upload_to='profile_pictures'),
        ),
        migrations.AddField(
            model_name='professor',
            name='my_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.Department'),
        ),
    ]
