$('.set-like-form').submit(function(e) {
    e.preventDefault();

    var this_form = $(this);
    var fields = this_form.serializeArray();

    $.ajax({
        type: 'POST',
        url: '',
        data: {
            csrfmiddlewaretoken: fields[0].value,
            'video_id': fields[1].value
        },
        success: function(result) {
            var p_div = this_form.parent();

            if(p_div.hasClass('like-active')) {
                p_div.removeClass('like-active');
                this_form.find('input[type=submit]').attr('value', '+');
            }
            else {
                p_div.addClass('like-active');
                this_form.find('input[type=submit]').attr('value', '-');
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});