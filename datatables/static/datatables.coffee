$(document).ready ->
  
  # $("select[data-updates-to]").live 'change', ->
  #   source_id = $(this).children?("option:selected").val()
  #   if not source_id then ""
  #   targets = $(this).data("updates-to").split(" ")
  #   target_infos = []
  #   for target in targets
  #     # target_info = target
  #     target_info = {}
  #     target_info.source_fk=target
  #     target_info.source_id=source_id
  #     
  #     $target=$("select[data-update-id='"+target+"']")
  #     update_info=$target.data($(this).data("update-id")).split(" ")
  #     
  #     target_info.update_id = $target.data("update-id")
  #     target_info.update_app = update_info[0]
  #     target_info.update_model = update_info[1]
  #     target_info.source_fk = update_info[2]
  #     target_info.generic_id = update_info?[3]
  #     target_info.generic_type = update_info?[4]
  #     
  #     target_info.update_filters = $(this).data?("update-filters")
  #     if not target_info.update_filters? then target_info.update_filters = ""
  #     target_info.empty_label = $target.data "empty-label"
  #     
  #     target_infos.push target_info
  # 
  #   $.ajax
  #     url: "/update_selects/"
  #     type: "GET"
  #     datatype: "json"
  #     contentType: "application/json",
  #     data: 
  #       selects: JSON.stringify target_infos
  #     success: (data) ->
  #       window.var=data
  #       $.each data, (select_option) ->
  #         select = data[select_option]
  #         options = "<option value=''>"+select.empty_label+"</option>"
  #         if select?.options.length
  #           select.options.map (option) ->
  #             options+="<option value='"+option.id+"'>"+option.name+"</option>"
  #         $("select[data-update-id='"+select_option+"']").html(options)?.trigger("liszt:updated")
  #     error: (data, status, error) ->
  #       console.log error, data.responseText
  #       
  # $('select').addClass("chzn-select").chosen();
  # $("select[data-updates]").change()