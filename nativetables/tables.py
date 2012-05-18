from bisect import bisect
from .features import BaseFeature, BaseFilter
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

class FeatureSet(list):
    def __unicode__(self):
        return mark_safe(''.join([item.__unicode__() for item in self]))

class DatatableOptions(object):
    def __init__(self, options=None):
        self.name = getattr(options, 'name', 'datatable')
        self.model = getattr(options, 'model', None)
        
class DatatableState(object):
    def __init__(self, state=None):
        self.search_param = getattr(state, 'search_param', '')
        self.filter_values = getattr(state, 'filter_values', {})
        self.ordering = getattr(state, 'ordering', {})
        self.page_number = getattr(state, 'page_number', 1)
        self.page = getattr(state, 'page', None)
        # self.fields = getattr(options, 'fields', None)
        # self.exclude = getattr(options, 'exclude', None)
        # self.widgets = getattr(options, 'widgets', None)

class DatatableMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_table = super(DatatableMetaclass, cls).__new__(cls, name, bases, attrs)
        features = attrs.get('features', FeatureSet(()))
        filters = attrs.get('filters', FeatureSet(()))
        for key, attr in attrs.items():
            # print key, attr
            if isinstance(attr, BaseFeature):
                # Populate a list of features that were declared
                attr.set_name(key)
                features.insert(bisect(features, attr), attr)
                if isinstance(attr, BaseFilter):
                    filters.insert(bisect(filters, attr), attr)
                    
        new_table.features=features
        new_table.filters=filters
        new_table._meta = DatatableOptions(getattr(new_table, 'Meta', None))
        new_table._state = DatatableState(getattr(new_table, 'Initial', None))
        return new_table

class BaseDatatable(Manager):
    def __init__(self, *args, **kwargs):
        super(BaseDatatable, self).__init__()
        self.keys=['id','features','filters','searches','orderings','pagination','searchable','orderable','paginate','paginator','state','initial']
        for key in self.keys:
            if not hasattr(self,key):
                setattr(self,key,None)
    def get_query_set(self):
        return DataSet(model=self.model, query=None, using=None,
                        keys=self.keys,
                        **{ key:getattr(self, key) for key in self.keys }
        )
    def transform(self, **kwargs):
        return self.get_query_set().transform(**kwargs)
                
class Datatable(BaseDatatable):
    __metaclass__ = DatatableMetaclass
    def __init__(self, *args, **kwargs):
        super(Datatable, self).__init__()
        # Pin Datatable to associated model
        self._meta.model.add_to_class(self._meta.name, self)
        # Give datatable model info for abstraction
        self.model = self._meta.model
        
class DataSet(QuerySet):
    ##########
    # Override base QuerySet methods to keep track of DataSet meta
    ##########
    def __init__(self, model, keys, query=None, using=None, **kwargs):
        super(DataSet, self).__init__(model, query, using)
        self.model = model
        self.keys=keys
        for key in keys:
            setattr(self,key,kwargs[key])
    
    def __getitem__(self, k):
        result = super(DataSet, self).__getitem__(k)
        return DataList(model=self.model, keys=self.keys, result=result, **{ key:getattr(self, key) for key in self.keys })
    
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
    
    # Modify datatable.state from a dict of options
    def update_state(self, **kwargs):
        
    
    # Apply pending changes to state
    def transform(self, **kwargs):
        search_param=kwargs.get('search_param',"")
        filter_values=kwargs.get('filter_values',{})
        ordering=kwargs.get('ordering',{})
        per_page=kwargs.get('per_page',20)
        page_number=kwargs.get('page_number',1)
        chain = self._clone()
        if getattr(self,'filters',False):
            chain = chain.filter_data(filter_values)
        if getattr(self,'searchable',False):
            chain = chain.search(search_param)
        if getattr(self,'orderable',False):
            chain = chain.order(ordering)
        if getattr(self,'paginate',False):
            chain = chain.paginate_data(per_page, page_number)
        return chain
    
    def filter_data(self, filter_values):
        print filter_values
        filter_args = {}
        for filter_field, selection in filter_values.iteritems():
            if filter_field in [f.name for f in self.filters]:
                if isinstance(selection, list):
                    filter_args[filter_field+"__in"]=selection
                else:
                    filter_args[filter_field]=selection
        print filter_args
        return self.filter(**filter_args) if filter_args else self
        
    def search(self, search_param):
        search_args = { search_field+"__icontains":search_param for search_field in self.searchable.split() }
        return self.filter(**search_args) if search_args else self
        
    def order(self, ordering):
        print ordering
        for order_field, direction in ordering.iteritems():
            order_args = ("-" if direction=="desc" else "")+order_field
        return self.order_by(order_args) if order_args else self
        
    def paginate_data(self, per_page, page_number):
        return self.paginator(self, per_page).page(page_number)
            

class DataList(list):
    ##########
    ## Override base list methods to keep track of DataList meta
    ##########
    def __init__(self, model, keys, result, **kwargs):
        list.__init__(self, result)
        self.model=model
        self.keys=keys
        for key in keys:
            setattr(self,key,kwargs[key])

    def __getitem__(self, k):
        result = super(DataList, self).__getitem__(k)
        return DataList(*result, keys=self.keys, **{ key:getattr(self, key) for key in self.keys })
        

def default_datatable(model):
    pass