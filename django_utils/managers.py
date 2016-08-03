# -*- coding: utf-8 -*-

import datetime

from django.db import models

# Right now these are duplicated because of various issues with recursive
# imports and different versions of Python
# TODO: Fix this so there's only one
DRAFT, HIDDEN, PUBLISHED = 'D', 'H', 'P'


class StatusManager(models.Manager):
    """ This adds a query methods to pull records based on status.
    """

    def draft(self):
        """ This adds a query method to pull all draft records.
        """
        return super(StatusManager, self).filter(
            status=DRAFT)

    def published(self):
        """ This adds a query method to pull all published records that are
        not expired.
        """
        today = datetime.date.today()

        return super(StatusManager, self).filter(
            status=PUBLISHED,
            pub_date__lte=today,
        ).filter(
            models.Q(expire_date__gt=today) |
            models.Q(expire_date__isnull=True)
        )

    def published_or_hidden(self):
        """ This adds a query method to pull all published or hidden records
        that are not expired
        """
        today = datetime.date.today()

        return super(StatusManager, self).filter(
            status__in=[
                PUBLISHED,
                HIDDEN
            ],
            pub_date__lte=today,
        ).filter(
            models.Q(expire_date__gt=today) |
            models.Q(expire_date__isnull=True)
        )
