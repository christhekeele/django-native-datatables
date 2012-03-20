from django.db import models
from django.db.models.query import QuerySet

class DatatableSet(QuerySet):
    ## kwargs are parsed table meta, holding a dictionary of dictionaries,
    ## mapping feature names to respective featuresets
    def __init__(self, model=None, query=None, **kwargs):
        super(DatatableSet, self).__init__(model, query)
        
    # def iterator(self):
    #     self.transform()
    #     return super(DatatableSet, self).iterator()
    #     
    # def transform(self):
    #     # take True values as having params, None values as default, do nothing if False
    #     if self.searching or self.searching is None: self.search()
    #     if self.filtering or self.filtering is None: self.filter()
    #     if self.ordering or self.ordering is None: self.order()
    #     if self.pagination or self.pagination is None: self.paginate()
    #     if self.selection or self.selection is None: self.select()

class DatatableManager(models.Manager):
    def get_query_set(self):
        return DatatableSet(self.model)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)
    def __getattr__(self, attr, *args):
        if attr.startswith("_"): # or at least "__"
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)