from django import template

register = template.Library()

censored_words = ['редиска',
                  'плохой',
                  'дурак']


@register.filter()
def censored_word(value):
    if not isinstance(value, str):
        raise ValueError(f"Фильтр применим только к строкам, получен {type(value)}")

    for word in censored_words:
        words = value.split()

        for i in range(len(words)):
            clean_word = words[i].strip('.,!?;:()[]{}"\'')
            if clean_word.lower() == word.lower():
                punctuation = words[i][len(clean_word):]
                words[i] = clean_word[0] + '*' * (len(clean_word) - 1) + punctuation
        value = ' '.join(words)

    return value
