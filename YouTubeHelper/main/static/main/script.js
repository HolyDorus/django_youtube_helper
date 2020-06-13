async function ld_SubmitHandler(event) {
    event.preventDefault();
    form = event.target;

    form_fields = form.children;

    const response = await fetch('../liked/', {
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
            alert(responseData.error);
            return;
        }

        icon = form.children[2].children[0];

        if (responseData.video_status == 'added') {
            if (icon.textContent == 'favorite_border'){
                icon.classList.remove('like-icon');
                icon.classList.add('dislike-icon');
                icon.textContent = 'favorite';
            }
        } else if (responseData.video_status == 'removed') {
            if (icon.textContent == 'favorite'){
                icon.classList.remove('dislike-icon');
                icon.classList.add('like-icon');
                icon.textContent = 'favorite_border';
            }
        }

        form_fields[2].blur();
    } else {
        console.log(`Error (${response.status}): ${response.statusText}`);  
    }
};


async function d_SubmitHandler(event) {
    event.preventDefault();
    
    if (!confirm("Вы точно хотите удалить это видео из списка 'Понравившиеся видео'?")) {
        return;
    }

    form = event.target;
    form_fields = form.children;

    const response = await fetch('../liked/', {
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
            alert(responseData.error);
            return;
        }

        if (responseData.video_status == 'removed') {
            block_success = document.querySelector('.block-status.b-success');
            block_success.classList.remove('visually-hidden');

            video_list = document.querySelector('.video-list');
            video_list.style.paddingTop = 0;

            video_title = form.parentElement.parentElement.children[0].children[0].textContent;

            ul = block_success.children[1];
            li = document.createElement('li');
            li.appendChild(document.createTextNode(`Видео "${video_title}" было удалено.`));
            ul.appendChild(li);

            form.parentElement.parentElement.parentElement.parentElement.parentElement.remove();
        }
    } else {
        console.log(`Error (${response.status}): ${response.statusText}`);  
    }
};


