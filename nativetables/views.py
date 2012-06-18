from django.core.exceptions import ImproperlyConfigured
from django.views.generic.list import MultipleObjectMixin, ListView
from django.core.paginator import Page

from django.utils import simplejson
import re

from .tables import default_datatable

class DatatableMixin(object):
    '''
    Requires MultipleObjectMixin derivative
    '''
    datatable = None
    context_datatable_name = None

    def get_queryset(self):
        """
        Return the datatable queryset class, transformed appropriately.
        """
        if self.datatable is not None:
            datatable_instance = self.datatable()
        # elif self.model is not None:
        #     datatable = default_datatable(self.model).all()
        else:
            raise ImproperlyConfigured(u"A datatable class was not specified. Define "
                                       u"%(cls)s.model to use the default or pass in your custom datatable through "
                                       u"%(cls)s.datatable"
                                       % {"cls": type(self).__name__})
        # Give datatable id so it can be referenced in html DOM elements
        datatable_instance.id = self.get_context_datatable_name(datatable_instance)
        return datatable_instance.all()

    def get_context_datatable_name(self, queryset):
        """
        Get the name to use for the table's template variable.
        If not provided, use underscored version of datatable class name
        """
        if self.context_datatable_name:
            context_datatable_name = self.context_datatable_name
        else:
            if hasattr(queryset,"object_list"):
                model = queryset.object_list.model
            else:
                model = queryset.model
            context_datatable_name = re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', model.__name__).lower().strip('_') + "_table"
        return context_datatable_name
        
    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        queryset = kwargs.pop('object_list')
        context_datatable_name = self.get_context_datatable_name(queryset)
        if queryset.paginate:
            page_obj = queryset.paginate_data()
            context = {
                'paginator': page_obj.paginator,
                'page_obj': page_obj,
                'is_paginated': True,
            }
            object_list = page_obj.object_list
            
            allow_empty = self.get_allow_empty()        
            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = len(self.object_list) == 0
                if is_empty:
                    raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                            % {'class_name': self.__class__.__name__})
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
            object_list = queryset

        if context_datatable_name is not None:
            context[context_datatable_name] = context['object_list'] = object_list
            
        context.update(kwargs)
        return context
        
        # return super(DatatableMixin, self).get_context_data(**context)
       
       
from base.helpers.django_utils import get_current_user
from company.models import Employee
class DatatableView(DatatableMixin, ListView):
    """
    Generic view that renders a template and passes in a ``Datatable`` object.
    """
    def get(self, request, *args, **kwargs):
        # If this is a page_load, inject a clean datatable into the session
        if not request.is_ajax():
            request.session['datatable'] = self.get_queryset()
            current_user = get_current_user()
            if not current_user.is_superuser:
                request.session['datatable']._state.filter_values['representative__employee'] = Employee.objects.get(user=current_user)
            else:
                request.session['datatable']._state.filter_values['representative__employee'] = None
        # Else, if there are ajax-requested changes in the GET data, update the table's state
        elif request.GET:
            # Pop the only table's changes from dict since datatableview only supports one datatable
            changes = simplejson.loads(request.GET.copy()['datatable_changes']).popitem()[1]
            request.session['datatable'] = request.session['datatable'].update_state(**changes)
            if 'representative__employee' not in request.session['datatable']._state.filter_values:
                current_user = get_current_user()
                if not current_user.is_superuser:
                    request.session['datatable']._state.filter_values['representative__employee'] = Employee.objects.get(user=current_user)
                else:
                    request.session['datatable']._state.filter_values['representative__employee'] = None

        self.object_list = request.session['datatable'].get_transformation()
        
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)