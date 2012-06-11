from django.utils.text import capfirst
from django.forms.forms import pretty_name
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template
from django.template import Template, Context
from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe

class BaseFeature(StrAndUnicode):
    "A base class used to identify Feature instances"
    creation_counter = 0
    name = None
    label=None
    default_template = None
    template = None
    context = None

    def __init__(self,**kwargs):
        self.label = kwargs.get('label',None)
        # Increase the creation counter, and save our local copy.
        self.creation_counter = BaseFeature.creation_counter
        self.context = {}
        BaseFeature.creation_counter += 1

    def __cmp__(self, other):
        # This is needed because bisect does not take a comparison function.
        return cmp(self.creation_counter, other.creation_counter)
    
    def set_name(self, name):
        self.name = name
        if self.label is None:
            self.label = capfirst(pretty_name(name))
    
    def __unicode__(self):
        self.context['name']=self.name
        self.context['label']=self.label
        named_context = Context(self.context)
        return mark_safe(get_template(self.template).render(named_context))

class BaseFilter(BaseFeature):
    choices = None
    "A base class used to identify Filter instances"
    def __init__(self, **kwargs):
        super(BaseFilter, self).__init__(**kwargs)

class BooleanFilter(BaseFilter):
    true_label = None
    false_label = None
    def __init__(self, **kwargs):
        super(BooleanFilter, self).__init__(**kwargs)
        self.context['true_label'] = self.true_label = kwargs.get('true_label', 'True')
        self.context['false_label'] = self.false_label = kwargs.get('false_label', 'False')
        self.default_template = 'bool_filter.html'
        self.template = kwargs.get('template', self.default_template)
        
class BaseModelFilter(BaseFilter):
    '''A Feature that filters model instances against a developer-provided model property pointing to another table'''
    model = None
    queryset = None
    filter_list = None
    name_field = None
    
    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        return queryset
        
    def __init__(self, **kwargs):
        super(BaseModelFilter, self).__init__(**kwargs)
        self.model = kwargs.get('model',None)
        self.queryset = kwargs.get('queryset',None)
        self.filter_list = self.get_queryset()
        self.name_field = kwargs.get('name_field',None)
        if self.name_field:
            self.choices = { item.id : getattr(item, self.name_field) for item in self.filter_list.only('id',self.name_field) }
        else:
            self.choices = { item.id : item for item in self.filter_list.only('pk') }
        self.context = dict(choices=self.choices)

class SingleModelFilter(BaseModelFilter):
    def __init__(self, **kwargs):
        super(SingleModelFilter, self).__init__(**kwargs)
        self.default_template = 'single_filter.html'
        self.template = kwargs.get('template', self.default_template)

class MultiModelFilter(BaseModelFilter):
    def __init__(self, **kwargs):
        super(MultiModelFilter, self).__init__(**kwargs)
        self.default_template = 'multi_filter.html'
        self.template = kwargs.get('template', self.default_template)

class SelectModelFilter(BaseModelFilter):
    def __init__(self, **kwargs):
        super(SelectModelFilter, self).__init__(**kwargs)
        self.default_template = 'select_filter.html'
        self.template = kwargs.get('template', self.default_template)

class MultiSelectModelFilter(BaseModelFilter):
    def __init__(self, **kwargs):
        super(MultiSelectModelFilter, self).__init__(**kwargs)
        self.default_template = 'multi_select_filter.html'
        self.template = kwargs.get('template', self.default_template)

class BaseSearch(BaseFeature):
    search_fields = None
    def __init__(self, **kwargs):
        super(BaseSearch, self).__init__(**kwargs)
        self.search_fields = kwargs.get('search_fields', None)
        
class Search(BaseSearch):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.default_template = 'search.html'
        self.template = kwargs.get('template', self.default_template)