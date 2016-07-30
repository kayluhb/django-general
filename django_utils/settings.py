# -*- coding: utf-8 -*-

from django.conf import settings


DJANGO_UTILS_PER_PAGE = getattr(
    settings, 'DJANGO_UTILS_PER_PAGE', 25)
DJANGO_UTILS_HTML5_DATE_FORMAT = getattr(
    settings, 'DJANGO_UTILS_HTML5_DATE_FORMAT', '%Y-%m-%d')
DJANGO_UTILS_HTML5_DATETIME_FORMAT = getattr(
    settings, 'DJANGO_UTILS_HTML5_DATETIME_FORMAT', '%Y-%m-%d %H:%M:%S')
