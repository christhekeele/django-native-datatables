$(document).ready ->
  tables = $('div:data("table")')
  changes = {}
  for datatable in tables
    $datatable = $(datatable)
    table_name = if $(tables).length > 1 then 'table' else $datatable.data("table")
    changes[table_name] = {}
        
    for single_filter in $datatable.find(':data("table-single-filter")')
      $(single_filter).find(':data("filter")').live 'click', ->
        $filter=$(this).closest(':data("table-single-filter")')
        if $filter.data('selected') != $(this).data('filter')
          $filter.data('selected', $(this).data('filter'))
        else
          $filter.data('selected', null)
        update_table table_name, 'single_filter', $filter.data('table-single-filter'), $filter.data('selected')
    
    for multi_filter in $datatable.find(':data("table-multi-filter")')
      $(multi_filter).find(':data("filter")').live 'click', ->
        $filter=$(this).closest(':data("table-multi-filter")')
        value_array = if $filter.data('selected') then $filter.data('selected').split(",") else []
        # for value, index in value_array
        #   value_array[index] = parseInt(value)
        if toString($(this).data('filter')) in value_array
          value_array.pop(toString($(this).data('filter')))
        else
          value_array.push(toString($(this).data('filter')))
        $filter.data('selected', value_array.join())
        update_table table_name, 'multi_filter', $filter.data('table-multi-filter'), value_array
        
    for single_select_filter in $datatable.find('select:data("table-select-filter")')
      $(single_select_filter).live 'change', ->
        update_table table_name, 'single_filter', $(this).data('table-select-filter'), $(this).val()
        
    for multi_select_filter in $datatable.find('select:data("table-multi-select-filter")')
      $(multi_select_filter).live 'change', ->
        update_table table_name, 'multi_filter', $(this).data('table-multi-select-filter'), $(this).val()
    
    $datatable.find(':data("table-search")').live 'keyup', ->
      update_table table_name, 'search', $(this).data('table-search'), $(this).val()
        
    $datatable.find(':data("table-order")').live 'click', ->
      default_order = 'asc'
      $(this).parent().children(':data("table-order")').removeClass('active')
      $(this).addClass('active')
      if not $(this).hasClass('asc') and not $(this).hasClass('desc')
        $(this).addClass(default_order)
      else
        $(this).toggleClass("asc desc")
      order = if $(this).hasClass('asc') then "asc" else "desc"
      update_table table_name, 'order', $(this).data('table-order'), order
    
    for paginate in $datatable.find(':data("table-paginate")')
      
      $(paginate).find(':data("per_page")').live 'click', ->
        update_table table_name, 'per_page', false, $(this).data('per_page')
        
      $(paginate).find(':data("page")').live 'click', ->
        update_table table_name, 'page', false, $(this).data('page')
    
  update_table = (table_name, action, target, value) ->
    console.log table_name, action, target, value
    changes[table_name]?['action']=action
    changes[table_name]?['target']=target
    changes[table_name]?['value']=value
    $.ajax
      url: ""
      type: "GET"
      datatype: "html"
      contentType: "application/json"
      data: 
        datatable_changes: JSON.stringify changes
      success: (data) ->
        table_body=$datatable.find(':data("table-content='+table_name+'")')
        table_body.html( $(data).find(':data("table-content='+table_name+'")').children() )
        table_pages=$datatable.find(':data("table-paginate='+table_name+'")')
        table_pages.html( $(data).find(':data("table-paginate='+table_name+'")').children() )
      # error: (data, status, error) ->
      #   console.log error, data.responseText