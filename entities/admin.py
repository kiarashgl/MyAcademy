from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Professor, Department, University


def make_verified(modeladmin, request, queryset):
	updated = queryset.update(verified=True)
	modeladmin.message_user(request, ngettext(
		'%d entity با موفقیت تایید شد.',
		'%d استاد با موفقیت تایید شدند.',
		updated,
	) % updated, messages.SUCCESS)


make_verified.short_description = "تایید entity های انتخاب شده"


def make_unverified(modeladmin, request, queryset):
	updated = queryset.update(verified=False)
	modeladmin.message_user(request, ngettext(
		'%d استاد با موفقیت عدم تایید شد.',
		'%d استاد با موفقیت عدم تایید شدند.',
		updated,
	) % updated, messages.SUCCESS)


make_unverified.short_description = "عدم تایید entity های انتخاب شده"


class EntityAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		try:
			return format_html('<img width="50" height="50" src="{}" />'.format(obj.picture.url))
		except:
			return format_html('<img width="50" height="50" src="/media/default_profile_picture.png" />')

	image_tag.short_description = 'Picture'


class ProfessorAdmin(EntityAdmin):
	list_display = ['name', 'image_tag', 'my_department', 'my_university', 'verified']
	list_filter = ['verified']
	search_fields = ['first_name', 'last_name']
	actions = [make_verified, make_unverified]

	def name(self, obj):
		return obj.first_name + " " + obj.last_name

	def my_university(self, obj):
		return obj.my_department.my_university


class DepartmentAdmin(EntityAdmin):
	list_display = ['name', 'image_tag', 'my_university', 'verified']
	list_filter = ['verified']
	search_fields = ['name']
	actions = [make_verified, make_unverified]


class UniversityAdmin(EntityAdmin):
	list_display = ['name', 'image_tag', 'address', 'verified']
	list_filter = ['verified']
	search_fields = ['name']
	actions = [make_verified, make_unverified]


admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(University, UniversityAdmin)
