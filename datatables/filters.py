from django.utils.text import capfirst
from django.forms.forms import pretty_name

class Filter(object):
    "A base class used to identify Filter instances"
    creation_counter = 0

    def __init__(self, label=None, **kwargs):
        self.label = label
        self.queryset = kwargs['queryset']
        self.template_name = kwargs.get('template_name','datatables/templates/filter.html')
        self.filter_choices = dict(item.id:item for item in queryset.only('id'))
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Filter.creation_counter
        Filter.creation_counter += 1

    def __cmp__(self, other):
        # This is needed because bisect does not take a comparison function.
        return cmp(self.creation_counter, other.creation_counter)
    
    def set_name(self, name):
        self.name = name
        if self.label is None:
            self.label = capfirst(pretty_name(name))
    
    def __unicode__(self):
        
        return mark_safe(u'<input%s />' % flatatt(final_attrs))