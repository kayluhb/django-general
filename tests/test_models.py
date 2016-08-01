#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-utils
------------

Tests for `django-utils` models module.
"""
import datetime

from django.test import TestCase

from django_utils.models import (
    DRAFT, HIDDEN, PUBLISHED, OrderedModel, StatusModel, TimeStampedModel)


class OrderedModelTest(OrderedModel):

    class Meta:
        app_label = 'django_utils'
        ordering = ('order',)


class StatusModelTest(StatusModel):

    class Meta:
        app_label = 'django_utils'


class TimeStampedModelTest(TimeStampedModel):

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

    def test_ordered_model_order(self):
        """ Test to see if ordered objects are ordered properly """
        ordered_model_1 = OrderedModelTest.objects.all()[0]
        ordered_model_2 = OrderedModelTest.objects.all()[1]
        ordered_model_3 = OrderedModelTest.objects.all()[2]

        self.assertEqual(ordered_model_1.order, 5)
        self.assertEqual(ordered_model_2.order, 10)
        self.assertEqual(ordered_model_3.order, 20)

    def test_status_model_default(self):
        """ Test the StatusModel default state """
        status_model = StatusModelTest.objects.all()[0]
        self.assertTrue(status_model.is_draft())

    def test_status_model_published(self):
        """ Test the StatusModel draft state """
        status_model = StatusModelTest.objects.filter(status=DRAFT)[0]
        self.assertTrue(status_model.is_draft())

    def test_status_model_hidden(self):
        """ Test the StatusModel hidden state """
        status_model = StatusModelTest.objects.filter(status=HIDDEN)[0]
        self.assertTrue(status_model.is_hidden())

    def test_status_model_published(self):
        """ Test the StatusModel published state """
        status_model = StatusModelTest.objects.filter(status=PUBLISHED)[0]
        self.assertTrue(status_model.is_published())

    def test_status_model_published_or_hidden(self):
        """ Test the StatusModel state change """
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
        self.assertTrue(not status_model.is_published())

    def test_timestamped(self):
        timestamped_model = TimeStampedModelTest.objects.create()
        self.assertTrue(timestamped_model)
        self.assertTrue(timestamped_model.created_at not None)
        self.assertTrue(timestamped_model.updated_at not None)

    def tearDown(self):
        pass
