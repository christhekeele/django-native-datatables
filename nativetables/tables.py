from bisect import bisect
import sys
from collections import OrderedDict
import inspect 
from .features import BaseFeature, BaseFilter, BaseSearch
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

class FeatureDict(OrderedDict):
    def __unicode__(self):
        return mark_safe(''.join([item.__unicode__() for item in self.values()]))

class DatatableOptions(object):
    def __init__(self, options=None):
        self.name = getattr(options, 'name', 'datatable')
        self.model = getattr(options, 'model', None)
        
class DatatableState(object):
    def __init__(self, state, paginate):
        self.search_values = getattr(state, 'search_values', {})
        self.filter_values = getattr(state, 'filter_values', {})
        self.ordering = getattr(state, 'ordering', {})
        if paginate:
            self.page_number = getattr(state, 'page_number', 1)
            self.per_page = getattr(state, 'per_page', 20)
        self.is_changed = True
        # self.fields = getattr(options, 'fields', None)
        # self.exclude = getattr(options, 'exclude', None)
        # self.widgets = getattr(options, 'widgets', None)
    
class DatatableMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(DatatableMetaclass, cls).__new__
        parents = [b for b in bases if isinstance(b, DatatableMetaclass)]
        if not parents:
            print "Sub"
            # If this isn't a subclass of Datatable, don't do anything special.
            # print super_new(cls, name, bases, attrs)
            return super_new(cls, name, bases, attrs)
        
        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        
        attr_meta = attrs.pop('Meta', None)
        new_class._meta=DatatableOptions(attr_meta)
        
        attr_state = attrs.pop('Initial', None)
        attr_paginate = attrs.pop('paginate', True)
        new_class._state=DatatableState(state=attr_state, paginate=attr_paginate)
        
        features = attrs.get('features', FeatureDict({}))
        filters = attrs.get('filters', FeatureDict({}))
        searches = attrs.get('searches', FeatureDict({}))
        for key, attr in attrs.items():
            if isinstance(attr, BaseFeature):
                # Populate a list of features that were declared
                attr.set_name(key)
                features[key] = attr
                if isinstance(attr, BaseFilter):
                    filters[key] = attr
                if isinstance(attr, BaseSearch):
                    searches[key] = attr
        
        new_class.features=features
        new_class.filters=filters
        new_class.searches=searches
        return new_class
        
class Datatable(Manager):
    __metaclass__ = DatatableMetaclass
    paginator = None
    
    def __init__(self, *args, **kwargs):
        super(Datatable, self).__init__()
        self.keys=['id','features','filters','searches','order_fields','pagination','paginate','paginator','_state']
        for key in self.keys:
            if not hasattr(self,key):
                setattr(self,key,None)
        if self.paginator is None:
            self.paginator = Paginator
        if self.paginate is None:
            self.paginate = True
            
        # Pin Datatable to associated model
        self._meta.model.add_to_class(self._meta.name, self)
        # Give datatable model info for abstraction
        self.model = self._meta.model
            
    def get_query_set(self):
        return DataSet(model=self.model, query=None, using=None,
                        keys=self.keys,
                        **{ key:getattr(self, key) for key in self.keys }
        )
        
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
    def update_state(self, action, target, value):
        print action, target, value
        is_different = False
        if action == 'search':
            is_different = True
            if target in self._state.search_values: del self._state.search_values[target]
            elif not hasattr(self._state.search_values, target) or value != getattr(self._state.search_values, target, None):
                self._state.search_values[target] = value
            else:
                is_different = False
                
        elif action == 'single_filter':
            is_different = True
            # IF the filter was set to empty
            if target in self._state.filter_values: del self._state.filter_values[target]
            # IF filter is applied for the first time or the filter isn't currently applied
            elif not hasattr(self._state.filter_values, target) or value != getattr(self._state.filter_values, target, None):
                self._state.filter_values[target] = value
            else:
                is_different = False
                
        elif action == 'multi_filter':
            is_different = True
            array = self._state.filter_values[target] if target in self._state.filter_values else []
            # If already in the array, remove it; or add it if not. (toggles)
            if value in array: array.remove(value)
            else: array.append(value)
            # If array is blank, delete the filter status entirely, else set it.
            if target in self._state.filter_values: del self._state.filter_values[target]
            else: self._state.filter_values[target] = array
                
        elif action == 'order':
            is_different = True
            if not target in self._state.ordering: self._state.ordering[target] = {}
            
            if self._state.ordering[target] == "desc": self._state.ordering = {target:"asc"}
            elif self._state.ordering[target] == "asc": self._state.ordering = {target:"desc"}
            else: self._state.ordering = {target:value}
                
        elif action == 'per_page':
            if self._state.per_page != value:
                self._state.per_page = value
                is_different = True
                
        elif action == 'page':
            if self._state.page_number != value:
                self._state.page_number = value
                is_different = True
        
        else:
            raise AttributeError, "'%s' datatable action is not supported. Refer to nativetables documentation for a list of valid options." % action
            
        if not action in ['order', 'page']:
            self._state.page_number = 1
            
        self._state.is_changed = is_different
        return self
        
    def get_transformation(self):
        chain = self._clone()
        if self._state.is_changed:
            if getattr(self,'filters', False):
                chain = chain.filter_data()
            if getattr(self,'searches', False):
                chain = chain.search()
            if getattr(self,'order_fields', False):
                chain = chain.order()
        return chain
    
    def filter_data(self):
        filter_args = {}
        for filter_field, selection in self._state.filter_values.iteritems():
            if filter_field in [f for f in self.filters]:
                if isinstance(selection, list):
                    filter_args[filter_field+"__in"]=selection
                else:
                    filter_args[filter_field]=selection
        return self.filter(**filter_args) if filter_args else self
        
    def search(self):
        search_args = {}
        for search_name, search_param in self._state.search_values.iteritems():
            if search_name in [s for s in self.searches]:
                for search_field in self.searches[search_name].search_fields:
                    search_args[search_field+"__icontains"] = search_param
        return self.filter(**search_args) if search_args else self
        
    def order(self):
        order_args = ""
        for order_field, direction in self._state.ordering.iteritems():
            if order_field in self.order_fields:
                order_args = ("-" if direction=="desc" else "")+order_field
        print order_args
        return self.order_by(order_args) if order_args else self
        
    def paginate_data(self):
        # print self.__class__
        # print self.paginator
        # print self._state.per_page
        # print self._state.page_number
        result = self.paginator(self, self._state.per_page)
        # print dir(result)
        # result.object_list.query.add_count_column()
        print result.object_list.query
        print result.object_list.query.get_count(using=result.object_list.db) 
        print result.object_list.count()
        ret = result.page(self._state.page_number)
        return ret
            

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