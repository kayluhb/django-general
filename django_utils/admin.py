# -*- coding: utf-8 -*-

import csv
from datetime import datetime

from django.http import HttpResponse
from django.general.translation import ugettext_lazy as _

from .models import DRAFT, HIDDEN, PUBLISHED


PUBLISHING_INFO = (
    _('Publishing Information'), {
        'fields': ['status', ('pub_date', 'expire_date'), 'slug'],
        'classes': ['collapse']
    }
)


def make_hidden(modeladmin, request, queryset):
    """ Publish all records in the query set
    """
    queryset.update(status=HIDDEN)
make_hidden.short_description = _("Mark selected as hidden")


def make_published(modeladmin, request, queryset):
    """ Publish all records in the query set
    """
    queryset.update(status=PUBLISHED)
make_published.short_description = _("Mark selected as published")


def make_unpublished(modeladmin, request, queryset):
    """ Publish all records in the query set
    """
    queryset.update(status=DRAFT)
make_unpublished.short_description = _("Mark selected as draft")


def export_select_fields_csv_action(
    description=_("Export objects as CSV file"), fields=None, exclude=None,
    header=True
):
    """
    This function returns an export csv action

    'fields' is a list of tuples denoting the field and label to be exported.
    Labels make up the header row of the exported file if header=True.

        fields=[
                ('field1', 'label1'),
                ('field2', 'label2'),
                ('field3', 'label3'),
            ]

    'exclude' is a flat list of fields to exclude. If 'exclude' is passed,
    'fields' will not be used. Either use 'fields' or 'exclude.'

        exclude=['field1', 'field2', field3]

    'header' is whether or not to output the column names as the first row

    Based on: http://djangosnippets.org/snippets/2020/
    """

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        date = datetime.strftime(datetime.now(), "%Y.%m.%d.%H%m")

        opts = modeladmin.model._meta

        field_names = [field.name for field in opts.fields]
        labels = []

        if exclude:
            field_names = [v for v in field_names if v not in exclude]
        elif fields:
            field_names = [k for k, v in fields]
            labels = [v for k, v in fields]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (
            unicode(opts).replace('.', '_'), date
        )

        writer = csv.writer(response)
        if header:
            if labels:
                writer.writerow(labels)
            else:
                writer.writerow(field_names)

        for obj in queryset:
            writer.writerow(
                [unicode(
                    getattr(obj, field)
                ).encode('utf-8') for field in field_names])

        return response

    export_as_csv.short_description = description
    return export_as_csv
