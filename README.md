# Django Datatables #
[![Build Status](https://secure.travis-ci.org/christhekeele/django-datatables.png)](http://travis-ci.org/christhekeele/django-datatables)

## WE ARE STILL DEEP IN DEVELOPMENT ##

### ANY ADVERTISED FEATURES MAY OR MAY NOT MERELY BE ON MY WHITEBOARD AT THE OFFICE ###

###### If you like what you see, watch this repo for updates. More watchers == more encouragement for me to get this thing out the door. ######

The goal of django-datatables is to integrate all the functionality of the [jquery datatables plugin](http://datatables.net) over a standard queryset workflow (`for object in object_list:`) with complete control over which features are implemented and how they are styled. Djagno-datatables is built to avoid deviating from standard django workflows, easily apply to existing apps, mixin cleanly into ListViews, and give maximum control to both back-end and front-end developers. By looping through an overridden, filtered queryset, nothing but what you see on a single page hits the database. Template tags use AJAX to update the queryset with new filters, avoiding full page reload. The end product is a polished, lightweight, natural django extension of your existing querysets.

## Features: ##

-  User-specified columns
-  Quick column filtering (ie: show only active users)
-  Customizable searching
-  By-column ordering
-  Low-load pagination
-  Per-record actions (ie: show, edit, delete)
-  Cross-table batch actions (all records, all records across pages, or all records on page)
-  Multiple datatables per page

## Components: ##

The app is broken down into three main parts.

-  A custom Queryset backend that contains all transformation features
-  A BaseForm-styled schema that cleanly and concisely configures datatables at the Model level
-  A suite of template tags per functionality that come with overridable default templates and AJAX updates

## Usage: ##

### Quickstart: ###

After adding 'django\_datatables' to your installed apps, just import and mixin the DatatableMixin into your ListView:

    from django_datatables.views import DatatableMixin
    class MyTableListing(DatatableMixin, ListView):

Or, just use the DatatableView:

    from django_datatables.views import DatatableView
    class MyTableListing(DatatableView):

Then add some template tags to your view so the default options will render, and link in some css and jquery:

    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}django_datables/themes/default.css" />
    <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
    {% load django_datatables %}
    {% datatable filters %}
    {% datatable search %}
    # Old content
    {% for object in object_list %}
      ....
    {% endfor %}
    
    {% datatable paginate %}

Spool up your runserver and check things out!

#### Behind the scenes ####

The quick start generates lot of functionality off of default values.

First, a custom Dataset extension of Queryset ties itself in to your ListView's object\_list.

Next, since no datatable was passed into the as\_view function, django-datatables will introspect your model and intuit some default functionality:

-  All columns will be displayed
-  Filters will be generated on boolean values
-  All text will be searchable
-  No columns will be orderable (so pre-existing table headers can be left alone)
-  The table will be paginated at 10 objects per page
-  No actions or batch actions will be available (for security reasons)

Finally, the template tags use their default templates wrapped in some AJAX to listen for user input and update the queryset in place.