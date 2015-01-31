$(document).ready ->
    $(document).on 'submit', 'form', (e) ->
        url = $(this).attr('action')
        parent = $(this).closest('.thing-name')
        e.preventDefault()
        $.ajax url,
            type: 'POST'
            dataType: 'json'
            data: $(this).serialize() + "&is_ajax=1"
            success: (data, status, jqXHR) ->
                parent.find('form').remove()
                parent.append(data.form)
