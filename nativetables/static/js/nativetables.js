// Generated by CoffeeScript 1.3.1
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  $(document).ready(function() {
    var $datatable, changes, datatable, multi_filter, multi_select_filter, paginate, single_filter, table_name, tables, update_table, _i, _j, _k, _l, _len, _len1, _len2, _len3, _len4, _m, _ref, _ref1, _ref2, _ref3;
    tables = $('div:data("table")');
    changes = {};
    for (_i = 0, _len = tables.length; _i < _len; _i++) {
      datatable = tables[_i];
      $datatable = $(datatable);
      table_name = $(tables).length > 1 ? 'table' : $datatable.data("table");
      changes[table_name] = {};
      _ref = $datatable.find(':data("table-single-filter")');
      for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
        single_filter = _ref[_j];
        $(single_filter).find(':data("filter")').live('click', function() {
          return update_table(table_name, 'single_filter', $(this).parent().data('table-single-filter'), $(this).data('filter') || null);
        });
      }
      _ref1 = $datatable.find(':data("table-multi-filter")');
      for (_k = 0, _len2 = _ref1.length; _k < _len2; _k++) {
        multi_filter = _ref1[_k];
        $(multi_filter).find(':data("filter")').live('click', function() {
          var value_array, _ref2;
          value_array = $.map($(this).parent().find(".active:data('filter')"), function(filter) {
            return $(filter).data('filter');
          });
          if (_ref2 = $(this).data('filter'), __indexOf.call(value_array, _ref2) >= 0) {
            value_array.pop($(this).data('filter'));
          } else {
            value_array.push($(this).data('filter'));
          }
          return update_table(table_name, 'multi_filter', $(this).parent().data('table-multi-filter'), value_array);
        });
      }
      _ref2 = $datatable.find('select:data("table-multi-select-filter")');
      for (_l = 0, _len3 = _ref2.length; _l < _len3; _l++) {
        multi_select_filter = _ref2[_l];
        $(multi_select_filter).live('change', function() {
          return update_table(table_name, 'multi_filter', $(this).data('table-multi-select-filter'), $(this).val());
        });
      }
      $datatable.find(':data("table-search")').live('keyup', function() {
        return update_table(table_name, 'search', $(this).data('table-search'), $(this).val());
      });
      $datatable.find(':data("table-order")').live('click', function() {
        var default_order, order;
        default_order = 'asc';
        $(this).parent().children(':data("table-order")').removeClass('active');
        $(this).addClass('active');
        if (!$(this).hasClass('asc') && !$(this).hasClass('desc')) {
          $(this).addClass(default_order);
        } else {
          $(this).toggleClass("asc desc");
        }
        order = $(this).hasClass('asc') ? "asc" : "desc";
        return update_table(table_name, 'order', $(this).data('table-order'), order);
      });
      _ref3 = $datatable.find(':data("table-paginate")');
      for (_m = 0, _len4 = _ref3.length; _m < _len4; _m++) {
        paginate = _ref3[_m];
        $(paginate).find(':data("per_page")').live('click', function() {
          return update_table(table_name, 'per_page', false, $(this).data('per_page'));
        });
        $(paginate).find(':data("page")').live('click', function() {
          return update_table(table_name, 'page', false, $(this).data('page'));
        });
      }
    }
    return update_table = function(table_name, action, target, value) {
      var _ref4, _ref5, _ref6;
      console.log(table_name, action, target, value);
      if ((_ref4 = changes[table_name]) != null) {
        _ref4['action'] = action;
      }
      if ((_ref5 = changes[table_name]) != null) {
        _ref5['target'] = target;
      }
      if ((_ref6 = changes[table_name]) != null) {
        _ref6['value'] = value;
      }
      return $.ajax({
        url: "",
        type: "GET",
        datatype: "html",
        contentType: "application/json",
        data: {
          datatable_changes: JSON.stringify(changes)
        },
        success: function(data) {
          var table_body, table_pages;
          table_body = $datatable.find(':data("table-content=' + table_name + '")');
          table_body.html($(data).find(':data("table-content=' + table_name + '")').children());
          table_pages = $datatable.find(':data("table-paginate=' + table_name + '")');
          return table_pages.html($(data).find(':data("table-paginate=' + table_name + '")').children());
        }
      });
    };
  });

}).call(this);
