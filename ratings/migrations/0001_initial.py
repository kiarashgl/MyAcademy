# Generated by Django 3.0.5 on 2020-05-28 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ratings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0009_auto_20200527_1749'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UniRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='محیط')),
                ('employment', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='اشتغال فارغ\u200cالتحصیلان')),
                ('dorm', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='خوابگاه')),
                ('accessibility', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='دسترسی آسان')),
                ('programs', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='فوق برنامه')),
                ('leisure', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='امکانات تفریحی')),
                ('uni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.University', verbose_name='دانشگاه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('knowledge', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='دانش و تخصص')),
                ('manners', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='اخلاق')),
                ('order', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='نظم و بابرنامگی')),
                ('attention', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='توجه به دانشجو')),
                ('teaching', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='کیفیت تدریس')),
                ('grading', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='نمره\u200cدهی')),
                ('load', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='حجم تمارین و پروژه\u200cها')),
                ('interesting', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='جذابیت کلاس')),
                ('research', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='توانایی در کارهای پژوهشی')),
                ('advice', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='راهنمایی\u200cهای مفید')),
                ('take_course_suggestion', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('research_suggestion', ratings.models.RatingField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Professor', verbose_name='استاد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeptRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='کیفیت آموزشی')),
                ('research', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='کیفیت پژوهشی')),
                ('update', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='اساتید به\u200cروز')),
                ('industry', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='ارتباط با صنعت')),
                ('lab', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='امکانات آزمایشگاهی')),
                ('programs', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='فوق برنامه')),
                ('flexibility', ratings.models.RatingField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='قوانین انعطاف پذیر')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Department', verbose_name='دانشکده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]