from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import DetailView

UNPUBLISHED_MESSAGE = _("This is not published. Only staff can view it.")


class StatusShowView(DetailView):
    """ Show the StatusModel
    """
    def add_menu(self):
        """ Add menu items to the django cms menu for the current object
        """
        meta = self.model._meta
        app_label = meta.app_label
        model_label = meta.verbose_name.capitalize()
        model_name = meta.verbose_name
        menu_key = '{}-menu'.format(app_label)
        menu_name = app_label.capitalize()
        menu = self.request.toolbar.get_or_create_menu(menu_key, menu_name)
        menu.add_break()
        menu.add_modal_item(
            'Change this {}'.format(model_label),
            url=reverse(
                'admin:{}_{}_change'.format(app_label, model_name),
                args=[self.object.id]
            )
        )
        menu.add_sideframe_item(
            'Delete this {}'.format(model_label),
            url=reverse(
                'admin:{}_{}_delete'.format(app_label, model_name),
                args=[self.object.id]
            )
        )

    def add_messages(self):
        """ Add a notification that the current object is not published
        """
        if not self.object.is_published_or_hidden():
            messages.info(self.request, UNPUBLISHED_MESSAGE)

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overridden.
        """
        if self.is_staff():
            return self.model._default_manager.all()
        return self.model._default_manager.published_or_hidden()

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(StatusShowView, self).get_context_data(**kwargs)

        if self.is_staff():
            self.add_menu()
            self.add_messages()

        return context

    def is_staff(self):
        """ Determine if the current logged in user is staff
        """
        return self.request.user.is_staff
