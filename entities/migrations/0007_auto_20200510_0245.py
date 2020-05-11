# Generated by Django 3.0.5 on 2020-05-09 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_professor_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='university',
            name='picture',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]