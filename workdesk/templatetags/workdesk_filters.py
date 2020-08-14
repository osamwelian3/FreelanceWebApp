from django import template

register = template.Library()


@register.filter(name='sizify')
def sizify(value):
    """
    simple kb/mb/Gb size snippet for templates
    {{ object.file.size|sizify }}
    """
    if value < 51200:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'Gb'
    return '%s %s' % (str(round(value, 2)), ext)


# register.filter('sizify', sizify)
