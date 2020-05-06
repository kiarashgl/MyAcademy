# Generated by Django 3.0.5 on 2020-05-06 13:45

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
                ('verified', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'دپارتمان',
                'verbose_name_plural': 'دپارتمان ها',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'دانشگاه',
                'verbose_name_plural': 'دانشگاه ها',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('my_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.Department')),
            ],
            options={
                'verbose_name': 'استاد',
                'verbose_name_plural': 'اساتید',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='my_university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.University'),
        ),
    ]
