# Django Datatables #
[![Build Status](https://secure.travis-ci.org/christhekeele/django-datatables.png)](http://travis-ci.org/christhekeele/django-datatables)

## __WE ARE STILL DEEP IN DEVELOPMENT__ ##

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