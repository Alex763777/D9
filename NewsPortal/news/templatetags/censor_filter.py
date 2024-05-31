from django import template

register = template.Library()

bad_words = {'редиска'}  # Определяем плохие слова как множество

@register.filter()
def censor(value):
    words = value.split()
    censored_text = ''

    for word in words:
        if word.lower() in bad_words:
            censored_word = word[0] + '*' * (len(word) - 1)    # Заменяем звездочками
            censored_text += censored_word + ' '
        else:
            censored_text += word + ' '

    return censored_text.rstrip()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()