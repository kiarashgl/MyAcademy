from django import template
from entities.models import Professor, Department, University

register = template.Library()


@register.filter(name='rating_path')
def rating_path(entity):
	if isinstance(entity, Professor):
		return 'ratings:professor_rating'
	if isinstance(entity, Department):
		return 'ratings:department_rating'
	if isinstance(entity, University):
		return 'ratings:university_rating'
	return ''


@register.filter(name='model_name')
def model_name(value):
	return value._meta.verbose_name.title()


@register.inclusion_tag('entities/university_card.html')
def render_university(university, dark=False):
	return {'entity': university, 'dark': dark}


@register.inclusion_tag('entities/department_card.html')
def render_department(department, dark=False):
	return {'entity': department, 'dark': dark}


@register.inclusion_tag('entities/professor_card.html')
def render_professor(professor, dark=False):
	return {'entity': professor, 'dark': dark}
