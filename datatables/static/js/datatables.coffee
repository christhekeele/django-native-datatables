$(document).ready ->
  tables = $('div:data("table")')
  for datatable in tables
    $datatable = $(datatable)
    table_name = if $(tables).length > 1 then 'table' else $datatable.data("table")
    window[table_name] = $datatable.data("table-state")
        
    for single_filter in $datatable.find(':data("table-single-filter")')
      $(single_filter).find(':data("filter")').live 'click', ->
        update_table table_name, 'single_filter', $(this).parent().data('table-single-filter'), $(this).data('filter')
    
    for multi_filter in $datatable.find(':data("table-multi-filter")')
      $(multi_filter).find(':data("filter")').live 'click', ->
        update_table table_name, 'multi_filter', $(this).parent().data('table-multi-filter'), $(this).data('filter')
    
    $datatable.find(':data("table-search")').live 'keyup', ->
      update_table table_name, 'search', false, $(this).val()
        
    $datatable.find(':data("table-order")').live 'click', ->
      default_order = 'asc'
      $(this).parent().children(':data("table-order")').removeClass('active')
      $(this).addClass('active')
      if not $(this).hasClass('asc') and not $(this).hasClass('desc')
        $(this).addClass(default_order)
      else
        $(this).toggleClass("asc desc")
      update_table table_name, 'order', $(this).data('table-order'), default_order
    
    for paginate in $datatable.find(':data("table-paginate")')
      
      $(paginate).find(':data("per_page")').live 'click', ->
        update_table table_name, 'per_page', false, $(this).data('per_page')
        
      $(paginate).find(':data("page")').live 'click', ->
        update_table table_name, 'page', false, $(this).data('page')
    
  update_table = (table_name, action, target, value) ->
    if action == 'search'
      window[table_name].search_param = value
      window[table_name].page_number = 1
      
    if action == 'single_filter'
      if not window[table_name]?.filter_values?[target]
        window[table_name].filter_values[target] = []
      array = window[table_name].filter_values[target]
      if value
        if not value in array else
          array.length = 0
          array.push(value)
      else
        array.length = 0
      window[table_name].page_number = 1
    
    if action == 'multi_filter'
      if not window[table_name]?.filter_values?[target]
        window[table_name].filter_values[target] = []
      array = window[table_name].filter_values[target]
      if value
        if value in array then array.splice(array.indexOf(value), 1) else array.push(value)
      else
          window[table_name].filter_values[target].length = 0
      window[table_name].page_number = 1
      
    if action == 'order'
      if window[table_name].ordering?[target] == "desc"
        window[table_name].ordering = {}
        window[table_name].ordering[target] = "asc"
      else if window[table_name].ordering?[target] == "asc"
        window[table_name].ordering = {}
        window[table_name].ordering[target] = "desc"
      else
        window[table_name].ordering = {}
        window[table_name].ordering[target] = value
      # window[table_name].page_number = 1
      
    if action == 'per_page'
      window[table_name].per_page = value
      window[table_name].page_number = 1
      
    if action == 'page'
      window[table_name].page_number = value
    
    $.ajax
      url: "/company/table/"
      type: "GET"
      datatype: "html"
      contentType: "application/json"
      data: 
        datatable: JSON.stringify window[table_name]
      success: (data) ->
        table_body=$datatable.find(':data("table-content='+table_name+'")')
        table_body.html( $(data).find(':data("table-content='+table_name+'")').children() )
        table_pages=$datatable.find(':data("table-paginate='+table_name+'")')
        table_pages.html( $(data).find(':data("table-paginate='+table_name+'")').children() )
      # error: (data, status, error) ->
      #   console.log error, data.responseText