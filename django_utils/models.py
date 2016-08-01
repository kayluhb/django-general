# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import StatusManager


# Use **BLANK instead of null=True, blank=True
BLANK = {'blank': True, 'null': True}

# Set up the statuses so they're globally accessible
DRAFT, HIDDEN, PUBLISHED = 'D', 'H', 'P'

STATUSES = (
    (HIDDEN, _("Hidden")),
    (DRAFT, _("Draft")),
    (PUBLISHED, _("Published")),
)


class OrderedModel(models.Model):
    """ An abstract model for ordering via an integer.
    """
    order = models.PositiveSmallIntegerField(
        _("Order"), default=1, help_text=("1 appears before 2")
    )

    class Meta:
        abstract = True
        ordering = ('order',)


class StatusModel(models.Model):
    """ This abstract model has the same properties as the Common Model, but it
    allows for statuses to be applied to the object.
    """
    expire_date = models.DateField(
        _("Expiration Date"), db_index=True, **BLANK)
    pub_date = models.DateField(
        _("Published Date"), db_index=True, default=datetime.date.today,
        help_text=_("Date to be published")
    )
    status = models.CharField(
        _("Status"), max_length=1, choices=STATUSES, default=DRAFT,
        help_text=_(
            "Hidden is publicly available, but not a part of the nav "
            "or lists. Draft hides it from unauthenticated users.")
    )

    # This must be RE-DECLARED in the inheriting class!
    objects = StatusManager()

    class Meta:
        abstract = True

    def is_published(self):
        """ Returns True if the object is published, and False otherwise.
        """
        today = datetime.date.today()
        return (
            self.status == PUBLISHED and
            self.pub_date <= today and

            # Not expired
            (self.expire_date is None or
                self.expire_date > today)
        )

    def is_draft(self):
        """ Returns True if object is draft
        """
        return self.status == DRAFT

    def is_hidden(self):
        """ Returns True if object is hidden
        """
        return self.status == HIDDEN

    def is_published_or_hidden(self):
        """ Returns True if the object is published or hidden, and False
        otherwise.
        """
        return self.is_hidden() or self.is_published()


class TimeStampedModel(models.Model):
    """ This is an abstract model which will be inherited by nearly all models.
    When the object is created it will get a created_at timestamp and each
    time it is modified it will receive a updated_at time stamp as well.
    """
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(
        _("Updated at"), auto_now=True, db_index=True, editable=False)

    class Meta:
        abstract = True
