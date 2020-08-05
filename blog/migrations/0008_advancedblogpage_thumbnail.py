# Generated by Django 3.0.5 on 2020-07-25 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('blog', '0007_blogpage_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancedblogpage',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
