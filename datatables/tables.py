# EXAMPLE DATATABLE

# from datatables.tables import Datatable
# class CompanyDatatable(Datatable):
#     filterable = "billing_status_id status_id priority_id"
#     searchable = "name"
#     orderable = "phone created_at updated_at"
#     paginate = True
#     initial = dict(search_param="",filter_values=dict(),ordering=dict(created_at="desc"),page_number=1,per_page=20)

from django.db.models import Manager
from django.db.models.query import QuerySet
from django.core.paginator import Paginator

class Datatable(Manager):
    state = {}
    def __init__(self, *args, **kwargs):
        super(Datatable, self).__init__()
        self.keys=['id','searchable','filterable','orderable','paginate','paginator','per_page','state','initial']
        for key in self.keys:
            if not hasattr(self,key):
                setattr(self,key,None)
        # self.state = dict(
        #             id=getattr(self,'id',""),
        #             searchable=getattr(self,'searchable',""),
        #             filterable=getattr(self,'filterable',""),
        #             orderable=getattr(self,'orderable',""),
        #             paginator=getattr(self,'paginator',Paginator),
        #             is_paginated=False
        #             initial=getattr(self,'initial',{})
        # )
    def get_query_set(self):
        return DataSet(model=self.model, query=None, using=None,
                        keys=self.keys,
                        **{ key:getattr(self, key) for key in self.keys }
        )
        

class DataSet(QuerySet):
    ##########
    # Override base QuerySet methods to keep track of DataSet meta
    ##########
    def __init__(self, keys, model=None, query=None, using=None, **kwargs):
        super(DataSet, self).__init__(model, query, using)
        self.keys=keys
        for key in keys:
            setattr(self,key,kwargs[key])
    
    def __getitem__(self, k):
        result = super(DataSet, self).__getitem__(k)
        return DataList(keys=self.keys, result=result, **{ key:getattr(self, key) for key in self.keys })
    
    def _clone(self, klass=None, setup=False, **kwargs):
        if klass is None:
            klass = self.__class__
        query = self.query.clone()
        if self._sticky_filter:
            query.filter_is_sticky = True
        c = klass(model=self.model, query=query, using=self._db, keys=self.keys, **{ key:getattr(self, key) for key in self.keys })
        c._for_write = self._for_write
        c._prefetch_related_lookups = self._prefetch_related_lookups[:]
        c.__dict__.update(kwargs)
        if setup and hasattr(c, '_setup_query'):
            c._setup_query()
        return c
    ##########
    # End overrides
    ##########
    
    def transform(self, **kwargs):
        search_param=kwargs.get('search_param',"")
        filter_values=kwargs.get('filter_values',{})
        ordering=kwargs.get('ordering',{})
        per_page=kwargs.get('per_page',20)
        page_number=kwargs.get('page_number',1)
        chain = self._clone()
        if getattr(self,'filterable',False):
            chain = chain.filter_data(filter_values)
        if getattr(self,'searchable',False):
            chain = chain.search(search_param)
        if getattr(self,'orderable',False):
            chain = chain.order(ordering)
        if getattr(self,'paginate',False):
            chain = chain.paginate_data(per_page, page_number)
        return chain
    
    def filter_data(self, filter_values):
        filter_args = { filter_field:selection for filter_field, selection in filter_values.iteritems() if filter_field in self.filterable and selection }
        return self.filter(**filter_args) if filter_args else self
        
    def search(self, search_param):
        search_args = { search_field+"__icontains":search_param for search_field in self.searchable.split() }
        return self.filter(**search_args) if search_args else self
        
    def order(self, ordering):
        order_args = [(("-" if direction=="desc" else "")+order_field) for order_field, direction in ordering.iteritems() if order_field in self.orderable]
        return self.order_by(*order_args) if order_args else self
        
    def paginate_data(self, per_page, page_number):
        return self.paginator(self, per_page).page(page_number)
            

class DataList(list):
    ##########
    ## Override base list methods to keep track of DataList meta
    ##########
    def __init__(self, keys, result, **kwargs):
        list.__init__(self, result)
        self.keys=keys
        for key in keys:
            setattr(self,key,kwargs[key])

    def __getitem__(self, k):
        result = super(DataList, self).__getitem__(k)
        return DataList(*result, keys=self.keys, **{ key:getattr(self, key) for key in self.keys })
        

def default_datatable(model):
    pass