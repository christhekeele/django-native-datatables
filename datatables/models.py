from django.db import models
from django.db.models.query import QuerySet

class DatatableSet(QuerySet):
    filtering, searching, ordering, pagination = None, None, None, None
    
    def __init__(self, query=None, **kwargs):
        super(DatatableSet, self).__init__(None, query)
        self.filtering = kwargs.get('filtering')
        self.searching = kwargs.get('searching')
        self.ordering = kwargs.get('ordering')
        self.pagination = kwargs.get('pagination')
        
    def iterator(self):
        chained_queryset = self.transform()
        return super(DatatableSet, chained_queryset).iterator()
        
    def transform(self):
        #copy self
        query=self.all()
        # take True values as having params, None values as default, do nothing if False
        if self.searching or self.searching is None:
            dataset = self.search(dataset)
        if self.filtering or self.filtering is None:
            dataset = self.filter(dataset)
        if self.ordering or self.ordering is None:
            dataset = self.order(dataset)
        if self.pagination or self.pagination is None:
            dataset = self.paginate(dataset)
        return dataset
    
    def update(self, transformation, option):
        pass

class Datatable(models.Manager):
    def get_query_set(self):
        return DatatableSet(self.query, self.filtering, self.searching, self.ordering, self.pagination)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"): # or at least "__"
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

class Datatable(object):
    # Implement ModelForms style structure here
    def __init__(self):
        pass