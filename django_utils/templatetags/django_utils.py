import re

from django.conf import settings
from django.core.cache import cache
from django.template import Library, TemplateSyntaxError

from ..pagination import PerPageNode


register = Library()

HTML5_DATE_FORMAT = settings.DJANGO_UTILS_HTML5_DATE_FORMAT
HTML5_DATETIME_FORMAT = settings.DJANGO_UTILS_HTML5_DATETIME_FORMAT


@register.simple_tag
def checked(value, dic):
    """ Returns ' checked' if the value is in the dictionary
    """
    return ' checked' if str(value) in dic else ''


@register.simple_tag
def on_class(value, dic):
    """ Returns 'class="on"' if the value is in the dictionary
    """
    return 'class="on"' if str(value) in dic else ''


@register.simple_tag
def date_tag(time, fmt="%m.%d.%Y", text=""):
    """ Returns an HTML5 time tag with the correct date format
    """
    if not time:
        return ""

    if not text:
        text = time.strftime(fmt)

    return time_tag(time, fmt, text, HTML5_DATE_FORMAT)


@register.simple_tag
def external_link_or_default(url, text, min_length):
    """ Returns an external link
    """
    if len(url) > min_length:
        return external_link(url, text)

    return external_link(url)


@register.simple_tag
def external_link(url, text="", klass=""):
    """ Returns a formatted link to an external URL
    """
    if url is None:
        return ""

    text = url.replace(
        'http://', ''
    ).replace(
        'https://', ''
    ).replace(
        'www.', ''
    ) if text == "" else text

    if url[0:4] != "http":
        url = 'http://' + url

    # remove a trailing slash if it exists
    if text[-1:] == "/":
        text = text[0:-1]

    klass = " class='{}'".format(klass) if klass != "" else ""

    return "<a href=\"{}\" target=\"_blank\" title=\"{}\"{}>{}</a>".format(
        url, text, klass, text
    )


@register.tag
def per_page_range(parser, token):
    """ Returns a PerPageNode
    """
    error = "{} takes the syntax {} number_to_iterate as context_variable"
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(error.format(fnctn, fnctn))
    if not trash == 'as':
        raise TemplateSyntaxError(error.format(fnctn, fnctn))
    return PerPageNode(num, context_name)


@register.simple_tag
def phone_number(text, delimeter="-"):
    """ Returns phone number from a string
    """
    if text is "" or text is None:
        return ""

    text = re.sub(r'[^0-9]', '', text)

    if text.startswith('1'):
        text = text[1:]

    phone = "<a class='phone' href='tel:{}'>{}{delimeter}{}{delimeter}{}</a>"

    return phone.format(
        text, text[0:3], text[3:6], text[6:], delimeter=delimeter
    )


@register.simple_tag
def time_tag(
    time,
    fmt="%b. %e, %Y %I:%M %p",
    text="",
    attr_fmt=HTML5_DATETIME_FORMAT
):
    """ Returns an HTML5 time tag with the correct date format
    """
    if not time:
        return ""

    if not text:
        text = time.strftime(fmt)

    return "<time datetime=\"{}\">{}</time>".format(
        time.strftime(attr_fmt),
        text
    )


@register.simple_tag
def url_replace(request, field, value):
    """ Method for replacing fields in the URL string
    """
    dict_ = request.GET.copy()
    if field == 'order_by' and field in dict_.keys():
        if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
            # click twice on same column, revert ascending/descending
            dict_[field] = value
        else:
            dict_[field] = "-"+value
    else:
        dict_[field] = value

    return dict_.urlencode()
