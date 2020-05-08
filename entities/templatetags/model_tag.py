from django import template


register = template.Library()

@register.filter(name='model_name')
def model_name(value):
	return value._meta.verbose_name.title()

@register.inclusion_tag('entities/university_card.html')
def render_university(university):
	return {'university' : university}

@register.inclusion_tag('entities/department_card.html')
def render_department(department):
	return {'department' : department}

@register.inclusion_tag('entities/professor_card.html')
def render_professor(professor):
	return {'professor' : professor}