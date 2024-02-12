function redirect(url) {
    window.location.href = url
}

function sendAjax({url, data, method = 'post', success, error}) {

    success = success || function (response) {
    }
    error = error || function (response) {
        createNotify(
            {
                title: 'ارور',
                message: 'مشکلی در ارسال درخواست وجود دارد لطفا اتصال خود را بررسی کنید',
                theme: 'error'
            }
        )
    }

    $.ajax(
        {
            url: url,
            data: JSON.stringify(data),
            type: method,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            },
            success: function (response) {
                success(response)
            },
            failed: function (response) {
                error(response)
            },
            error: function (response) {
                error(response)
            }
        }
    )
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
}

function randomString(length = 15) {
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


function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function removeCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


function createLoading(element, options = {
    size: 'normal',
    color: '#1ee696',
    fill: null

}) {
    if (element.classList.contains('loading-element-parent')) {
        return
    }
    let loading = document.createElement('div')
    loading.className = `loading-element loading-circle-${options.size}`
    let color = options.color
    loading.style = `
        border-top-color:${color};
        border-right-color:${color};
    `
    let loading_blur = document.createElement('div')
    if (options.fill) {
        loading_blur.style = `
            background:${options.fill};
        `
        loading_blur.classList.add('fill')
    }
    loading_blur.className = 'loading-blur-element'
    element.append(loading_blur)
    element.append(loading)
    element.classList.add('loading-element-parent')
    element.setAttribute('disabled', 'disabled')
}

function removeLoading(element) {
    try {
        element.querySelector('.loading-element').remove()
        element.querySelector('.loading-blur-element').remove()
        element.classList.remove('loading-element-parent')
        element.removeAttribute('disabled')
    } catch (e) {

    }
}


let all_datetime_convert = document.querySelectorAll('.datetime-convert')
for (let dt_el of all_datetime_convert) {
    let dt = dt_el.innerHTML || dt_el.value
    dt_el.setAttribute('datetime', dt)
    let dt_persian = new Date(dt).toLocaleDateString('fa-IR', {
        // hour: '2-digit',
        // minute: '2-digit'
    });
    dt_persian = dt_persian.replaceAll('/', '-')
    if (dt_persian != 'Invalid Date') {
        dt_el.innerHTML = dt_persian
        dt_el.value = dt_persian
    }
}

let all_spread_price = document.querySelectorAll('.spread-price')
for (let el of all_spread_price) {
    let price = el.innerHTML
    el.innerHTML = numberWithCommas(price)
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// ---


let container_select_choices = document.querySelectorAll('.container-select-choices')

$('.container-select-choices input[type="radio"]').on('change', function (e) {
    let inp = e.currentTarget
    let choices = inp.parentNode.parentNode
    choices.setAttribute('choice-val', inp.value)

});


// price elements
document.querySelectorAll('.price-el').forEach((el) => {
    let p = el.innerText
    el.setAttribute('price-val', p)
    el.innerHTML = numberWithCommas(p)
})

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function getRandomString(length) {
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

// random-bg
document.querySelectorAll('.random-bg').forEach(function (el) {
    el.style.background = getRandomColor()
})


function toggleRelatedField(fieldId, show = true) {
    const field = document.getElementById(fieldId);
    if (show) {
        field.classList.remove('d-none');
    } else {
        field.classList.add('d-none');
    }
}

// add query params
let query_params = (new URL(location)).searchParams;
document.querySelectorAll('.add-params-to-href').forEach(function (el) {
    let href = el.getAttribute('href')
    let href_params = new URLSearchParams(href)
    for (let p of query_params) {
        let k = p[0]
        let v = String(p[1])
        if (href.includes(k) === false) {
            href_params.set(k, v)
        }
    }
    let params = href_params.toString()
    if (params.indexOf('?') == -1) {
        params = '?' + params
    }
    el.setAttribute('href', params)
})

document.querySelectorAll('.add-params-to-form').forEach(function (form) {
    for (let p of query_params) {
        let name = p[0]
        let value = p[1]
        if (!form.elements[name]) {
            let inp = document.createElement('input')
            inp.type = 'hidden'
            inp.name = name
            inp.value = value
            form.appendChild(inp)
        }
    }
})

// select option by filter query search
document.querySelectorAll('.select-by-filter').forEach(function (select) {
    let filter_name = select.name || select.getAttribute('filter-name')
    let filter_value = getUrlParameter(filter_name)
    try {
        select.querySelector(`[value="${filter_value}"]`).setAttribute('selected', 'selected')
    } catch (e) {
    }
})

// select option by value select
document.querySelectorAll('.select-by-value').forEach(function (select) {
    let value = select.getAttribute('value') || 'false'
    if (value == 'False') {
        value = 'false'
    } else if (value == 'True') {
        value = 'true'
    }
    try {
        select.querySelector(`option[value="${value}"]`).setAttribute('selected', 'selected')
    } catch (e) {
    }
})

// theme(dark mode)

let _btn_switch_theme = document.querySelector('.dark-switch')
try {
    _btn_switch_theme.addEventListener('click', function (el) {
        el.preventDefault()
        if (el.currentTarget.classList.contains('active')) {
            setThemeMode('light')
        } else {
            setThemeMode('dark')
        }
    })
} catch (e) {
}
function setThemeMode(theme) {
    setCookie('theme-mode', theme)
    if (theme === 'light') {
        _btn_switch_theme.classList.remove('active')
        document.body.classList.remove('dark-mode')
    } else {
        _btn_switch_theme.classList.add('active')
        document.body.classList.add('dark-mode')
    }
}

// initial theme
setThemeMode(getCookie('theme-mode') || 'light')

