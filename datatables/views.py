import math

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import ListView

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def datatable(table_name, **kwargs):
    # find by the table name
    base_list = Company.objects.all()
    # "search param"
    search = kwargs.get('search', "")
    # { filter_name: selection, filter_name: selection }
    filters = kwargs.get('filters', {})
    # "-column_name"
    ordering = kwargs.get('ordering', "")
    # { page_by: num, page: num }
    pagination = kwargs.get('pagination', {page_by: 20, page: 1})
    # return pagination extrema?
    full_list = base_list.filter(name__icontains=search).filter(**filters).order_by(ordering)#[pagination['start'] : pagination['end']]
    paginated_list = Paginator(qs, pagination['page_by'])
    try
        object_list = pqs.page(pagination["page"])
    except PageNotAnInteger:
        object_list = pqs.page(1)
    except EmptyPage:
        object_list = pqs.page(pqs.num_pages)
    # find by table name
    template = "whatever.html"
    return render_to_response(template, {'object_list':object_list})
