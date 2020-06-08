from django import template

register = template.Library()


@register.inclusion_tag('comment.html')
def render_comment(rating):
	return {
		'content': rating.comment,
		'first_name': rating.user.first_name,
		'last_name': rating.user.last_name,
		'picture': rating.user.profile_picture.url,
		'date': rating.date,
		'pk': rating.pk,

		'likes': rating.liked_users.count,
		'like_url': rating.get_like_url,

		'dislikes': rating.disliked_users.count,
		'dislike_url': rating.get_dislike_url,
	}
