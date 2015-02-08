$(document).ready ->
    $(document).on 'click', '.container a.email', (e) ->
        url = $(this).attr('href')
        msg = $(this).closest('.msg')
        e.preventDefault()
        $.ajax url,
            type: 'GET'
            dataType: 'json'
            data: $(this).serialize()
            success: (data, status, jqXHR) ->
                msg.empty().append(data.msg)
