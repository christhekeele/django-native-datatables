from django.db import models
from django.db.models.query import QuerySet

class DatatableSet(QuerySet):
    filterable, searchable, orderable, initial = None, None, None, None
    
    def __init__(self, query=None, **kwargs):
        super(DatatableSet, self).__init__(None, query)
        self.filterable = kwargs.get('filterable')
        self.searchable = kwargs.get('searchable')
        self.orderable = kwargs.get('orderable')
        self.initial = kwargs.get('initial')
        
    # def iterator(self):
    #     chained_queryset = self.transform()
    #     return super(DatatableSet, chained_queryset).iterator()
        
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
        return self.filter(**{ search_field+"__icontains":search_param for search_field in self.searchable })
        
    def filter(self, filter_values):
        return self.filter(**{ filter_field:selection for filter_field, selection in filter_values.iteritems() if filter_field in self.filterable })
    
    def order(self, ordering):
        return self.order_by(*[ (("-" if direction=="desc" else "")+order_field) for order_field, direction in ordering.iteritems() if order_field in self.orderable ])

class Datatable(models.Manager):
    def get_query_set(self):
        # In the future this will go through all fields and create appropriate objects for filterable, sortable, searchable
        # In the meantime just provide pre-formatted versions of these on the subclass definition
        return DatatableSet(self.query, self.filterable, self.searchable, self.orderable, self.initial)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"): # or at least "__"
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

def default_datatable(model):
    pass

# class CompanyDatatable(datatables.Datatable):
#     filterable = "billing_status_id status_id priority_id"
#     searchable = "name"
#     orderable = "phone created_at updated_at"
#     initial = dict(search_param="",filter_values=dict(active=True),ordering=dict(created_at="desc"))