# -*- coding: utf-8 -*-

import datetime

from django.db import models

# from django_utils.models import (PUBLISHED, DRAFT, HIDDEN)


class StatusManager(models.Manager):
    """ This adds a query methods to pull records based on status.
    """

    def draft(self):
        """ This adds a query method to pull all draft records.
        """
        return super(StatusManager, self).filter(
            status=django_utils.models.DRAFT)

    def published(self):
        """ This adds a query method to pull all published records that are
        not expired.
        """
        today = datetime.date.today()

        return super(StatusManager, self).filter(
            status=django_utils.models.PUBLISHED,
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
                django_utils.models.PUBLISHED,
                django_utils.models.HIDDEN
            ],
            pub_date__lte=today,
        ).filter(
            models.Q(expire_date__gt=today) |
            models.Q(expire_date__isnull=True)
        )
