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
        print order_args
        print self.query
        if order_args:
            return self.order_by(*order_args)
        else:
            return self

class Datatable(Manager):
    def get_query_set(self):
        # In the future this will go through all fields and create appropriate objects for filterable, sortable, searchable
        # In the meantime just provide pre-formatted versions of these on the subclass definition
        return DatatableSet(self.model, filterable=self.filterable, searchable=self.searchable, orderable=self.orderable, initial=self.initial)
    def transform(self, **kwargs):
        return DatatableSet(self.model, filterable=self.filterable, searchable=self.searchable, orderable=self.orderable, initial=self.initial).transform(**kwargs)
    # def __getattr__(self, name):
    #     return getattr(self.get_query_set(), name)
    # def __getattr__(self, attr, *args):
    #     if attr.startswith("_"): # or at least "__"
    #         raise AttributeError
    #     return getattr(self.get_query_set(), attr, *args)

def default_datatable(model):
    pass

# class CompanyDatatable(datatables.Datatable):
#     filterable = "billing_status_id status_id priority_id"
#     searchable = "name"
#     orderable = "phone created_at updated_at"
#     initial = dict(search_param="",filter_values=dict(active=True),ordering=dict(created_at="desc"))