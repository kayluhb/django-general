# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext


def get_status_list_or_404(model, **kwargs):
    """ Attempts to get a list of objects in the given model with
    the given kwargs, but also checks if they're published. This
    will raise a 404 error if the list is empty.
    """
    objs = model.objects.published().filter(**kwargs)

    try:
        assert objs.exists()

    except AssertionError:
        raise Http404

    else:
        return objs


def get_status_object_or_404(model, **kwargs):
    """ Checks for an object in the given model with the given
    kwargs, but also checks if it's published. This will raise
    a 404 if the object does not exist.
    """
    try:
        obj = model.objects.published_or_hidden().get(**kwargs)

    except model.DoesNotExist:
        raise Http404

    else:
        return obj


def render_response(request, *args, **kwargs):
    """ Render a response with the given context
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
