from django import template

register = template.Library()


@register.inclusion_tag('comment.html')
def render_comment(rating, user):
	return {
		'content': rating.comment,
		'full_name': rating.user.get_full_name(),
		'picture': rating.user.get_profile_picture_url,
		'date': rating.date,
		'pk': rating.pk,

		'likes': rating.liked_users.count,
		'liked': user in rating.liked_users.all(),
		'like_url': rating.get_like_url,

		'dislikes': rating.disliked_users.count,
		'disliked': user in rating.disliked_users.all(),
		'dislike_url': rating.get_dislike_url,
	}
