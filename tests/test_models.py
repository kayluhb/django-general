#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-utils
------------

Tests for `django-utils` models module.
"""
import datetime

from django.db import models
from django.test import TestCase

from django_utils.models import (
    DRAFT, HIDDEN, PUBLISHED, OrderedModel, StatusModel, TimeStampedModel)


class OrderedModelTest(OrderedModel):
    """ An implementation of the OrderedModel abstract class
    """

    class Meta:
        app_label = 'django_utils'
        ordering = ('order',)


class StatusModelTest(StatusModel):
    """ An implementation of the StatusModel abstract class
    """

    class Meta:
        app_label = 'django_utils'


class TimeStampedModelTest(TimeStampedModel):
    """ An implementation of the TimeStampedModel abstract class
    """
    title = models.CharField(blank=True, max_length=255)

    class Meta:
        app_label = 'django_utils'


class TestDjangoUtils(TestCase):

    def setUp(self):
        OrderedModelTest.objects.create(order=10)
        OrderedModelTest.objects.create(order=20)
        OrderedModelTest.objects.create(order=5)

        StatusModelTest.objects.create()
        StatusModelTest.objects.create(status=PUBLISHED)
        StatusModelTest.objects.create(status=HIDDEN)

        TimeStampedModelTest.objects.create()

    def test_ordered_model_order(self):
        """ Test to see if ordered objects are ordered properly
        """
        ordered_model_1 = OrderedModelTest.objects.all()[0]
        ordered_model_2 = OrderedModelTest.objects.all()[1]
        ordered_model_3 = OrderedModelTest.objects.all()[2]

        self.assertEqual(ordered_model_1.order, 5)
        self.assertEqual(ordered_model_2.order, 10)
        self.assertEqual(ordered_model_3.order, 20)

    def test_status_model_default(self):
        """ Test the StatusModel default state
        """
        status_model = StatusModelTest.objects.all()[0]
        self.assertTrue(status_model.is_draft())

    def test_status_model_draft(self):
        """ Test the StatusModel draft state
        """
        status_model = StatusModelTest.objects.filter(status=DRAFT)[0]
        self.assertTrue(status_model.is_draft())

    def test_status_model_hidden(self):
        """ Test the StatusModel hidden state
        """
        status_model = StatusModelTest.objects.filter(status=HIDDEN)[0]
        self.assertTrue(status_model.is_hidden())

    def test_status_model_published(self):
        """ Test the StatusModel published state
        """
        status_model = StatusModelTest.objects.filter(status=PUBLISHED)[0]
        self.assertTrue(status_model.is_published())

    def test_status_model_published_or_hidden(self):
        """ Test the StatusModel state change
        """
        status_model = StatusModelTest.objects.filter(status=PUBLISHED)[0]
        self.assertTrue(status_model.is_published_or_hidden())
        status_model.status = HIDDEN
        self.assertTrue(status_model.is_published_or_hidden())

    def test_expire_date(self):
        """ Test the expiration date """
        yesterday = datetime.date.today() - datetime.timedelta(1)
        status_model = StatusModelTest.objects.filter(status=PUBLISHED)[0]
        status_model.pub_date = yesterday
        status_model.expire_date = yesterday
        self.assertFalse(status_model.is_published())

    def test_timestamped(self):
        """ Test the auto-population of TimeStampedModels
        """
        timestamped_model = TimeStampedModelTest.objects.all()[0]
        self.assertIsNotNone(timestamped_model.created_at)
        self.assertIsNotNone(timestamped_model.updated_at)

    def test_timestamped_updated_at_change(self):
        """ Test that the updated_at property changes when a model is saved.
        """
        timestamped_model = TimeStampedModelTest.objects.all()[0]
        updated_at = timestamped_model.updated_at
        timestamped_model.title = 'Foo bar'
        timestamped_model.save()

        self.assertNotEqual(timestamped_model.updated_at, updated_at)

    def tearDown(self):
        pass
