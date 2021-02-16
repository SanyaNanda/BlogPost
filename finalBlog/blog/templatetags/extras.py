from django import template
import readtime

register = template.Library()

@register.filter(name='get_val')
def get_val(dict, key):
	return dict.get(key)


def read(html):
    return readtime.of_html(html)

register.filter('readtime',read)