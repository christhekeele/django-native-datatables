$(document).ready ->
  tables = $('div:data("table")')
  changes = {}
  for datatable in tables
    $datatable = $(datatable)
    table_name = if $(tables).length > 1 then 'table' else $datatable.data("table")
    changes[table_name] = {}
        
    for single_filter in $datatable.find(':data("table-single-filter")')
      $(single_filter).find(':data("filter")').live 'click', ->
        update_table table_name, 'single_filter', $(this).parent().data('table-single-filter'), $(this).data('filter')
    
    for multi_filter in $datatable.find(':data("table-multi-filter")')
      $(multi_filter).find(':data("filter")').live 'click', ->
        update_table table_name, 'multi_filter', $(this).parent().data('table-multi-filter'), $(this).data('filter')
    
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
      update_table table_name, 'order', $(this).data('table-order'), default_order
    
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