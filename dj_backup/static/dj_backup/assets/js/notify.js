
function createNotify({
    title, message, theme, positionClass='nfc-top-right', closeOnClick=true, showDuration=6500
}) {
    // delete old notify elements
    document.querySelectorAll('.ncf-container').forEach((e) => {
        e.remove()
    })
    let id = `notify-${random_string(10)}`
    let notify_el = document.createElement('div')
    notify_el.id = `${id}`
    notify_el.className = `ncf-container ${positionClass}`

    let notify_el_content = ``
    if (theme == 'error'){
        notify_el_content = `
             <div class="alert alert-fill alert-danger alert-icon">
                 <em class="icon ni ni-cross-circle"></em>
                 ${message || ''}
             </div>
        `
    }else if (theme == 'success'){
        notify_el_content = `
            <div class="alert alert-fill alert-success alert-icon">
                <em class="icon ni ni-check-circle"></em> 
                ${message || ''}
            </div>
        `
    }else if (theme == 'warning'){
        notify_el_content = `
            <div class="alert alert-fill alert-warning alert-icon">
                <em class="icon ni ni-alert-circle"></em>
                ${message || ''}
            </div>
        `
    }

    notify_el.innerHTML = notify_el_content

    document.body.append(notify_el)
    let element = document.getElementById(id)
    if (closeOnClick) {
        element.addEventListener('click', function () {
            element.remove()
        })
    }
    let show_duration_timeout = null
    try {
        clearTimeout(show_duration_timeout)
    } catch (e) {
    }
    show_duration_timeout = setTimeout(function () {
        element.remove()
    }, showDuration,)
}


function random_string(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}
