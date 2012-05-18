# Django Native Datatables #
[![Build Status](https://secure.travis-ci.org/christhekeele/django-native-datatables.png)](http://travis-ci.org/christhekeele/django-native-datatables)

## V0.9 underway ##

### I reccommend waiting for V1.0 before playing with the code, and V1.1 before trying to apply to a project ###

###### If you like what you see, watch this repo for updates. More watchers == more encouragement for me to get this thing out the door. ######

The goal of django-native-datatables is to implement all the functionality of the [jquery datatables plugin](http://datatables.net) over a standard ListView queryset workflow (`for object in object_list`) with complete control over which features are implemented and how they are styled. Django-datatables is built to avoid deviating from standard django workflows, easily apply to existing apps, mixin cleanly into ListViews, and give maximum control to both back-end and front-end developers. By looping through an overridden, filtered queryset, nothing but what you see on a single page hits the database. Template tags use AJAX to update the queryset with new filters, avoiding full page reload. The end product is a polished, lightweight, natural django extension of your existing querysets.

## Features: ##

-  Diverse chainable filtering (show only active users, with either a cat or a dog as a pet, who work for pet store x)
-  Customizable live searching
-  By-column ordering
-  Low-load pagination
-  Multiple datatables per page
-  ListView integration
-  Hooks into your own custom view functions:
   -  Per-table actions (ie: new, export, import)
   -  Per-record actions (ie: show, edit, delete)
   -  Batch actions across selected records (ie: export, delete, deactivate, change owner)

### How django-native-datatables differs from datatables.net: ###

-  __There's no need to hook into the ORM yourself.__  
   Django-native-datatables automatically passes all the AJAX parameters to it's own custom queryset (Dataset) that calls a transformation function before rendering. The transformation method calls other method to apply queryset filters, one method per feature, leveraging all the power of Django's querysets for you. The filters are chained resulting in a single, specific query that hits the database exactly how it needs to, no more and no less.
-  __Each datatable can be customized from a simple schema.__  
   Simply define which fields and features you want to expose on a model in a `ModelForm` inspired schema and pass it to the view's `as_view()`. The transformation methods will listen to the schema and apply (or disable) features as requested.
-  __All transformation methods are overrideable if necessary.__  
   If all these customizations still aren't doing it for you, you can read through the documented source code and override it the way you want easily, the way class-based views are meant to work.
-  __You can cherrypick datatable features and use your own solutions for others.__  
   Since all django-datatables does is add a transformation step to the standard `for object in object_list:` workflow, other plugins meant to wrap around this workflow (say, [django-endless-pagination](http://django-endless-pagination.readthedocs.org/en/latest/)) will function cleanly if the datatable's default pagination is turned off.
-  __You can control every element of the styling.__  
   `object_list` is still yours to break down and display, but much like a `ModelForm` your customized search bars, filters, etc will be available as `{{ object_list.awesome_filter }}` with an overrideable template used in the rendering, or like `ModelForm`s you can break it down manually like `{{ for option in object_list.awesome_filter }}`.
   
### How django-native-datatables works like datatables.net: ###

-  All of the same features are available.
-  Interfacing with the datatable uses AJAX, keeping the entire page from reloading.
   
## Core Components: ##

The app is broken down into several main parts.

-  A custom Queryset backend that knows how to keep track of its state and perform transformations on itself
-  A group of Features that function like django Fields
-  A user-defined ModelForm-style schema that cleanly and concisely configures datatables at the Model level
-  A suite of templates that Features use to render themselves by default
-  A jQuery script that knows how to listen to all of the rendered Features on the page for changes, and AJAXs in the result
-  A DatatableMixin for pages with only one datatable

## Usage: ##

### Quickstart: ###

Download django-native-datatables and add `nativetables` to your installed apps.

Use the DatatableView in your urls.py instead of a ListView, with slightly different paramerters:

    from nativetables.views import DatatableView
    urlpatterns = patterns('awesome.views',
        ....
        url(r'^table/$',
            DatatableView.as_view(
                template_name = "awesome/index.html",
                datatable = default_datatable(model=Awesome),
            ),
            name='awesome_index'
        ),
        ....
    )

Then include jQuery and the nativetables.js, and enjoy the new features around your old template:

    <script src="/path/to/jquery.js" type="text/javascript"></script>
    <script src="/path/to/nativetables.js" type="text/javascript"></script>
    
    {{ object_list.filters }}
    {{ object_list.search_bar }}
    
    # Old content
    {% for object in object_list %}
      ....
    {% endfor %}
    
    {{ object_list.pagination }}

Spool up your runserver and check things out!

#### Behind the scenes ####

The quick start generates lot of functionality off of default values.

First, the `default_datatable()` function introspects your model, and creates a `Datatable` object with default filters, searching, ordering, and pagination that inherits from django's `Manager` class.

By default:

-  Filters will be generated on boolean values, `CharField`s using `choices`, and `ForeignKey` fields with 10 items or less in the table
-  A searchbar will be provided across all text fields
-  No columns will be orderable (so pre-existing table headers can be left alone)
-  The table will be paginated
-  No actions or batch actions will be available (for security reasons)
-  An initial state will be assigned to the table:
   - Page number: 1
   - Per page: 20
   - Filtering: `active`=True, if it exists on the model

In the view function, the `Datatable` manager transforms itself based on the default feature settings and the initial state, returning a queryset called `object_list`.

In the template, the Features attributes of your `object_list` render themselves automatically, with hooks for the jQuery script.

If the state of the table is changed through the Features attributes, jQuery will send the new state to your view functions, and replace the table data with the results of the modified queryset.

## Development: ##

As I am producing this on my own, for only one of my projects at work, feature development may be slow. However, my co-workers and I are likely to use it in future projects down the line, so bug/error/optimization improvements will be ongoing.

All issues are appreciated, and any pull requests are welcome. Check the Milestones for a roadmap of development, and chip in if you feel like it!