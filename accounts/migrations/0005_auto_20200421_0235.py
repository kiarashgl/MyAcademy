# Generated by Django 3.0.5 on 2020-04-20 22:05

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('accounts', '0004_remove_user_is_moderator'),
	]

	operations = [
		migrations.AddField(
			model_name='user',
			name='bio',
			field=models.CharField(blank=True, max_length=100),
		),
		migrations.AddField(
			model_name='user',
			name='major',
			field=models.CharField(blank=True, max_length=100),
		),
		migrations.AddField(
			model_name='user',
			name='profile_picture',
			field=models.ImageField(default='default_profile_picture.png', upload_to='profile_pictures'),
		),
		migrations.AddField(
			model_name='user',
			name='university',
			field=models.CharField(blank=True, max_length=100),
		),
	]
