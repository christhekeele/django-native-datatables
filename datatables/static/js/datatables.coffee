$(document).ready ->
  tables = $('div:data("table")')
  for datatable in tables
    $datatable = $(datatable)
    table_name = if $(tables).length > 1 then 'table' else $datatable.data("table")
    window[table_name] = $datatable.data("table-state")
    
    for filter in $datatable.find(':data("table-filter")')
      $filter = $(filter)
      filter_name = $filter.data('table-filter')
      $filter.find(':data("filter")').live 'click', ->
        update_table table_name, 'filter', filter_name, $(this).data('filter')
    
    for search in $datatable.find(':data("table-search")')
      $(search).find(':data("search")').live 'keyup', ->
        update_table table_name, 'search', false, $(search).find(':data("search")').val()
    
    for paginate in $datatable.find(':data("table-paginate")')
      
      $(paginate).find(':data("per_page")').live 'click', ->
        update_table table_name, 'per_page', false, $(this).data('per_page')
        
      $(paginate).find(':data("page")').live 'click', ->
        update_table table_name, 'page', false, $(this).data('page')
    
  update_table = (table_name, action, target, value) ->
    console.log table_name, action, target, value
    if action == 'search'
      window[table_name].search_param = value
      window[table_name].page_number = 1
      
    if action == 'filter'
      if window[table_name].filter_values[target]
        window[table_name].filter_values[target] = ""
      else
        window[table_name].filter_values[target] = value
      window[table_name].page_number = 1
      
    if action == 'order'
      window[table_name].ordering[target] = value
      window[table_name].page_number = 1
      
    if action == 'per_page'
      window[table_name].per_page = value
      window[table_name].page_number = 1
      
    if action == 'page'
      window[table_name].page_number = value
    
    console.log window[table_name]
    
    $.ajax
      url: "/company/table/"
      type: "GET"
      datatype: "html"
      contentType: "application/json",
      data: 
        datatable: JSON.stringify window[table_name]
      success: (data) ->
        table_body=$datatable.find(':data("table-content='+table_name+'")')
        table_body.html( $(data).find(':data("table-content='+table_name+'")').children() )
        table_pages=$datatable.find(':data("table-paginate='+table_name+'")')
        table_pages.html( $(data).find(':data("table-paginate='+table_name+'")').children() )
      error: (data, status, error) ->
        console.log error, data.responseText