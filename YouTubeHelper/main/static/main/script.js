// $('.set-like-form').submit(function(e) {
//     e.preventDefault();

//     var this_form = $(this);
//     var fields = this_form.serializeArray();

//     $.ajax({
//         type: 'POST',
//         url: '',
//         data: {
//             csrfmiddlewaretoken: fields[0].value,
//             'video_id': fields[1].value
//         },
//         success: function(result) {
//             var p_div = this_form.parent();

//             if(p_div.hasClass('like-active')) {
//                 p_div.removeClass('like-active');
//                 this_form.find('input[type=submit]').attr('value', '+');
//             }
//             else {
//                 p_div.addClass('like-active');
//                 this_form.find('input[type=submit]').attr('value', '-');
//             }
//         },
//         error: function(xhr, errmsg, err) {
//             console.log(xhr.status + ": " + xhr.responseText);
//         }
//     });
// });


async function myFormSubmitHandler(event) {
    event.preventDefault();
    form = event.target;
    form_fields = form.children;

    const response = await fetch('/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json',
            'X-CSRFToken': form_fields[0].value
        },
        body: JSON.stringify({
            'video_id': form_fields[1].value
        })
    });

    const responseData = await response.text();

    if (response.ok) {
        console.log(responseData);
    } else {
        console.log('Error!SAD!'); 
    }

    alert('Good');
};