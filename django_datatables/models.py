from django.db import models
from django.db.models.query import QuerySet

class DatatableSet(QuerySet):
    ## kwargs are parsed table meta, holding a dictionary of dictionaries,
    ## mapping feature names to respective featuresets
    def __init__(self, query=None, datatable=None):
        super(DatatableSet, self).__init__(None, query)
        self.selection = datatable.get('selection', None)
        self.filtering = datatable.get('filtering', None)
        self.searching = datatable.get('searching', None)
        self.ordering = datatable.get('ordering', None)
        self.pagination = datatable.get('pagination', None)
        
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
        if self.selection or self.selection is None:
            dataset = self.select(dataset)
        return dataset
    
    def update(self, transformation, option):
        pass

class DatatableManager(models.Manager):
    def get_query_set(self):
        return DatatableSet(self.query)
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