# -*- coding: utf-8 -*-

import datetime

from django.db import models

from . import models


class StatusManager(models.Manager):
    """ This adds a query method to pull all published records. """
    def published(self):
        today = datetime.date.today()

        return super(StatusManager, self).filter(
            status=models.PUBLISHED,
            pub_date__lte=today,
        ).filter(
            models.Q(expire_date__gt=today) |
            models.Q(expire_date__isnull=True)
        )

    def published_or_hidden(self):
        today = datetime.date.today()

        return super(StatusManager, self).filter(
            status__in=[models.PUBLISHED, models.HIDDEN],
            pub_date__lte=today,
        ).filter(
            models.Q(expire_date__gt=today) |
            models.Q(expire_date__isnull=True)
        )
