async function myFormSubmitHandler(event) {
    event.preventDefault();
    form = event.target;
    form_fields = form.children;

    const response = await fetch('liked/', {
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

    const responseData = await response.json();

    if (response.ok) {
        if (responseData.error) {
            console.log('Error: ' + responseData.error); 
        }

        if (responseData.video_status == 'added') {
            if (!form.parentElement.classList.contains('like-active')) {
                form.parentElement.classList.add('like-active');
                form_fields[2].value ='-';
            }
        } else if (responseData.video_status == 'removed') {
            if (form.parentElement.classList.contains('like-active')) {
                form.parentElement.classList.remove('like-active');
                form_fields[2].value ='+';
            }
        }

        form_fields[2].blur();

        // form.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
    } else {
        console.log(`Error (${response.status}): ${response.statusText}`);  
    }
};