# EXAMPLE DATATABLE

# from datatables.tables import Datatable
# class CompanyDatatable(datatables.Datatable):
#     filterable = "active priority"
#     searchable = "name description email"
#     orderable = "created_at updated_at acquired_on"
#     initial = dict(search_param="",filter_values=dict(active=True),ordering=dict(acquired_on="desc"))

from django.db.models import Manager
from django.db.models.query import QuerySet

class DatatableSet(QuerySet):
    filterable, searchable, orderable, initial = None, None, None, None
    
    def __init__(self, model=None, query=None, using=None, **kwargs):
        super(DatatableSet, self).__init__(model, query, using)
        self.filterable = kwargs.get('filterable')
        self.searchable = kwargs.get('searchable')
        self.orderable = kwargs.get('orderable')
        self.initial = kwargs.get('initial')
        
    def transform(self, **kwargs):
        search_param=kwargs.get('search_param',"")
        filter_values=kwargs.get('filter_values',{})
        ordering=kwargs.get('ordering',"")
        # take True values as having params, None values as default, do nothing if False
        if self.searchable or self.searchable is None:
            dataset = self.search(search_param)
        if self.filterable or self.filterable is None:
            dataset = self.filter(filter_values)
        if self.orderable or self.orderable is None:
            dataset = self.order(ordering)
        return dataset
    
    def search(self, search_param):
        if search_param:
            return self.filter(**{ search_field+"__icontains":search_param for search_field in self.searchable.split() })
        else:
            return self
        
    def filter(self, filter_values):
        filter_args = { filter_field:selection for filter_field, selection in filter_values.iteritems() if filter_field in self.filterable }
        if filter_args:
            return self.filter(**filter_args)
        else:
            return self
    
    def order(self, ordering):
        order_args = [(("-" if direction=="desc" else "")+order_field) for order_field, direction in ordering.iteritems() if order_field in self.orderable]
        if order_args:
            return self.order_by(*order_args)
        else:
            return self

class Datatable(Manager):
    def get_query_set(self):
        return DatatableSet(self.model, filterable=self.filterable, searchable=self.searchable, orderable=self.orderable, initial=self.initial)
    def transform(self, **kwargs):
        return DatatableSet(self.model, filterable=self.filterable, searchable=self.searchable, orderable=self.orderable, initial=self.initial).transform(**kwargs)

def default_datatable(model):
    pass