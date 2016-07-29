# -*- coding: utf-8 -*-
from django.conf import settings


DJANGO_UTILS_PER_PAGE = getattr(settings, 'DJANGO_UTILS_PER_PAGE', 25)
