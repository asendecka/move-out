$(document).ready ->
    $(document).on 'click', '.is-gone', (e) ->
        form = $(this).closest('.thing').find('form')
        img = $(this).find('img')
        e.preventDefault()
        form.submit()
        img.toggleClass('gone')
