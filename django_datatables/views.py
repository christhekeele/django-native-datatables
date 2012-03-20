from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView

from django_datatables.models import DatatableSet

class DatatableMixin(object):
    '''
    Requires MultipleObjectMixin derivative
    '''
    datatable_class = None
    datatable_options = None
    context_datatable_name = None

    def get_datatable_options(self):
        """
        Return a table object to use. The table has automatic support for
        sorting and pagination.
        """
        options = {}
        datatable_class = self.get_datatable_class()
        # options = datatable_class.to_dict
        return options

    def get_datatable_class(self):
        """
        Return the class to use for the table.
        """
        if self.datatable_class:
            return self.datatable_class
        raise ImproperlyConfigured(u"A table class was not specified. Define "
                                   u"%(cls)s.table_class"
                                   % {"cls": type(self).__name__})

    def get_context_table_name(self, table):
        """
        Get the name to use for the table's template variable.
        """
        return self.context_datatable_name or "datatable"
    
    def get_object_list(self):
        if not hasattr(self, "object_list"):
            raise ImproperlyConfigured(u"Query-set like variable object_list was not specified. Define "
                                   u"%(cls)s.object_list"
                                   % {"cls": type(self).__name__})
        elif not hasattr(self, "get_queryset"):
            raise ImproperlyConfigured(u"DatatableMixin must be employed with a child of MultipleObjectMixin.")
        else:
           # Our new object list, instance of DatatableSet
           object_list = DatatableSet(self.get_queryset(), self.get_datatable_options())

    def get_context_data(self, **kwargs):
       """
       Overriden version of ``MultipleObjectMixin`` to inject the datatable into
       the template's context.
       """
       context = super(DatatableMixin, self).get_context_data(**kwargs)
       object_list = self.get_object_list()
       context[self.get_context_table_name(object_list)] = object_list
       return context
       
class DatatableView(DatatableMixin, ListView):
   """
   Generic view that renders a template and passes in a ``DatatableSet`` object.
   """