# -*- coding: utf-8 -*-

from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .settings import DJANGO_UTILS_PER_PAGE


PER_PAGE = DJANGO_UTILS_PER_PAGE


def get_pager_params(get):
    """ Build our parameters for the pagination
    """
    try:
        page = int(get.get('page', 1))

    except ValueError:
        page = 1

    try:
        per_page = int(get.get('per_page', 1))

    except ValueError:
        per_page = PER_PAGE

    allowed_per_pages = [x * PER_PAGE + PER_PAGE for x in range(8)]

    if per_page not in allowed_per_pages:
        per_page = PER_PAGE

    if get.get('page'):
        # This is so we can keep our query parameters.
        # We have to copy it because it's immutable.
        query_remainder = get.copy()
        # delete the page param because we're going to give it a new one.
        del query_remainder[u'page']
        # Munge it into a string.
        query_remainder = query_remainder.urlencode(True)
    else:
        query_remainder = get.urlencode

    return page, per_page, query_remainder


def normalize(current, all_pages):
    """ Normalize pagination
    """
    _min = 1

    if current == 1:
        _max = min(current + 5, all_pages[-1] + 1)

    elif current == 2:
        _max = min(current + 4, all_pages[-1] + 1)

    elif current > all_pages[-1] - 5:
        _max = all_pages[-1] + 1
        _min = max(all_pages[-1] - 5, 1)

    else:
        _max = min(current + 3, all_pages[-1])
        _min = max(current - 2, 1)

    return range(_min, _max)


def paginate(records, page, per_page):
    """ Paginate our records
    """

    paginator = Paginator(records, per_page)
    try:
        records = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)

    return records
