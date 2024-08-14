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

document.querySelectorAll('.spread-num-el').forEach((el) => {
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


function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

document.querySelectorAll('.file-size-convert').forEach(function (el) {
    let unit = el.getAttribute('data-unit') || 'Bytes'
    let size = el.getAttribute('data-size')

    if (unit == 'KB') {
        size = size * 1000
    }
    el.innerHTML = formatBytes(size)
})


let FILE_EXTENSIONS = {
    'video': ['mp4', 'mkv'],
    'audio': ['mp3', 'wav', 'ogg'],
    'image': ['png', 'jpg'],
    'zip': ['zip', 'rar'],
    'text': ['text', 'txt', 'doc'],
    'folder': [],
}

function setFileIcons() {
    document.querySelectorAll('.icon-by-extension').forEach(function (el) {
        // TODO: should be completed
        let extension = el.getAttribute('extension')
        // TODO: use by dict not if statement
        let extension_icons = {}

        if (extension == '') {
            el.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 72 72">
                        <path fill="#6C87FE" d="M57.5,31h-23c-1.4,0-2.5-1.1-2.5-2.5v-10c0-1.4,1.1-2.5,2.5-2.5h23c1.4,0,2.5,1.1,2.5,2.5v10
                        C60,29.9,58.9,31,57.5,31z"></path>
                        <path fill="#8AA3FF" d="M59.8,61H12.2C8.8,61,6,58,6,54.4V17.6C6,14,8.8,11,12.2,11h18.5c1.7,0,3.3,1,4.1,2.6L38,24h21.8
                        c3.4,0,6.2,2.4,6.2,6v24.4C66,58,63.2,61,59.8,61z"></path>
                         <path display="none" fill="#8AA3FF" d="M62.1,61H9.9C7.8,61,6,59.2,6,57c0,0,0-31.5,0-42c0-2.2,1.8-4,3.9-4h19.3
                        c1.6,0,3.2,0.2,3.9,2.3l2.7,6.8c0.5,1.1,1.6,1.9,2.8,1.9h23.5c2.2,0,3.9,1.8,3.9,4v31C66,59.2,64.2,61,62.1,61z"></path>
                        <path fill="#798BFF" d="M7.7,59c2.2,2.4,4.7,2,6.3,2h45c1.1,0,3.2,0.1,5.3-2H7.7z"></path>
                  </svg>
                `
        } else if (extension == 'sqlite') {
            el.innerHTML = `
                   <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="transform: scale(1.3)"  viewBox="0 -142 512 512"  preserveAspectRatio="xMidYMid">
                        <defs>
                                <linearGradient x1="57.6615627%" y1="2.04644676%" x2="57.6615584%" y2="94.4387516%" id="linearGradient-1">
                                    <stop stop-color="#97D9F6" offset="0%">
                        
                        </stop>
                              <stop stop-color="#0F80CC" offset="92.024499%">
                        </stop>
                            <stop stop-color="#0F80CC" offset="100%">
                        </stop>
                                </linearGradient>
                        </defs>
                        <g>
                        <path d="M194.519337,112.044206 C187.698564,112.044206 182.152486,114.063211 177.900552,118.099455 C173.648619,122.139234 171.491713,127.434452 171.491713,133.922666 C171.491713,137.285148 172.027403,140.350953 173.082873,143.160235 C174.138343,145.975174 175.780773,148.582909 177.98895,150.939241 C180.197127,153.297694 184.617017,156.501413 191.20442,160.5746 C199.287514,165.509134 204.577238,169.513908 207.116022,172.640884 C209.656575,175.765215 210.917127,179.03947 210.917127,182.453039 C210.917127,187.023558 209.412597,190.671912 206.320442,193.414365 C203.222983,196.158062 199.080663,197.524862 193.944751,197.524862 C188.527735,197.524862 183.809061,195.6153 179.756906,191.823204 C175.704751,188.025635 173.659227,183.002703 173.61326,176.707182 L171.093923,176.707182 L171.093923,199.558011 L173.61326,199.558011 C174.38232,197.394203 175.44663,196.287293 176.839779,196.287293 C177.509834,196.287293 179.079779,196.749436 181.524862,197.61326 C187.474033,199.730026 192.358895,200.751381 196.198895,200.751381 C202.816354,200.751381 208.464972,198.433775 213.171271,193.723757 C217.870497,189.015874 220.243094,183.337017 220.243094,176.707182 C220.243094,171.56632 218.676685,166.992435 215.60221,163.005539 C212.527735,159.013848 206.548508,154.370829 197.61326,149.038688 C189.92442,144.419175 184.933481,140.65681 182.629834,137.723771 C180.322652,134.794961 179.138122,131.555204 179.138122,128.000014 C179.138122,124.154703 180.550718,121.066084 183.337017,118.762438 C186.123315,116.457024 189.774144,115.314924 194.342541,115.314924 C199.483757,115.314924 203.769282,116.84067 207.160221,119.911609 C210.547624,122.987852 212.506519,127.250747 213.082873,132.729296 L215.60221,132.729296 L215.60221,112.928184 L213.259669,112.928184 C212.97326,113.937687 212.708066,114.58299 212.464088,114.872935 C212.227182,115.161112 211.77105,115.314924 211.093923,115.314924 C210.278895,115.314924 208.825635,114.971941 206.762431,114.29835 C202.342541,112.809731 198.267403,112.044206 194.519337,112.044206 L194.519337,112.044206 Z M276.861878,112.044206 C268.550718,112.044206 261.005083,114.003101 254.187845,117.922659 C247.36,121.835145 241.955359,127.268073 237.966851,134.187859 C233.98011,141.107101 232,148.455772 232,156.287307 C232,166.808751 235.443978,176.182269 242.38674,184.39779 C249.333039,192.608361 257.656575,197.724471 267.314917,199.690608 C269.523094,200.841193 272.682431,203.811359 276.81768,208.618785 C281.478011,214.044103 285.420552,217.957127 288.662983,220.287293 C291.901878,222.618689 295.398895,224.327425 299.093923,225.458564 C302.792486,226.584935 306.791602,227.138122 311.116022,227.138122 C316.352707,227.138122 321.041326,226.227978 325.171271,224.353591 L324.243094,222.055249 C321.845746,222.919963 319.289282,223.337017 316.596685,223.337017 C312.94232,223.337017 309.249061,222.131978 305.546961,219.712707 C301.850166,217.287425 297.226961,212.660162 291.712707,205.834254 C289.120884,202.563536 287.331713,200.499978 286.320442,199.690608 C296.887514,197.62705 305.577017,192.505635 312.353591,184.309392 C319.128398,176.116685 322.519337,166.766518 322.519337,156.287307 C322.519337,143.84459 318.092376,133.387499 309.303867,124.861886 C300.508287,116.335388 289.691934,112.044206 276.861878,112.044206 L276.861878,112.044206 Z M328.265193,112.044206 L328.397719,114.740339 C333.931421,114.740339 337.030648,116.370394 337.723686,119.646416 C337.981808,120.818571 338.100261,122.982902 338.121476,126.099455 L338.077348,185.723757 C338.031381,190.176884 337.396685,193.02011 336.176796,194.254144 C334.955138,195.479337 332.890166,196.24663 329.900552,196.552486 L329.768027,199.248619 L384.928248,199.248619 L386.342612,185.723757 L383.823275,185.723757 C383.103717,189.408177 381.454214,192.047565 378.8288,193.546961 C376.196314,195.057319 371.541286,195.801105 364.81775,195.801105 L359.602281,195.801105 C353.552336,195.801105 350.051783,193.61396 349.127143,189.21547 C348.936203,188.345282 348.870789,187.412324 348.861949,186.38674 L349.082944,126.099455 C349.081529,121.653399 349.643386,118.67404 350.806701,117.215477 C351.982391,115.762217 354.10217,114.948957 357.171341,114.740339 L357.038815,112.044206 L328.265335,112.044206 L328.265193,112.044206 Z M277.745856,115.314924 C287.119558,115.314924 294.773039,119.00677 300.685083,126.453046 C306.595359,133.901988 309.524862,144.111211 309.524862,157.038688 C309.524862,169.288656 306.552928,179.097289 300.596685,186.475138 C294.640442,193.850696 286.712928,197.524862 276.861878,197.524862 C267.398011,197.524862 259.723315,193.736133 253.834254,186.121547 C247.950497,178.506961 245.038674,168.620906 245.038674,156.464103 C245.038674,143.971727 247.985856,133.971631 253.922652,126.497245 C259.855912,119.030814 267.801105,115.314924 277.745856,115.314924 L277.745856,115.314924 Z M404.596685,128.132611 C403.251271,128.132611 402.225856,128.586975 401.458564,129.502777 C400.673591,130.415028 400.433149,131.52 400.707182,132.861893 C400.972376,134.163631 401.706077,135.3045 402.872928,136.265208 C404.032707,137.22501 405.28442,137.723771 406.629834,137.723771 C407.93105,137.723771 408.922873,137.225038 409.635359,136.265208 C410.347845,135.3045 410.565304,134.163631 410.298343,132.861893 C410.024309,131.52 409.315359,130.415028 408.220994,129.502777 C407.114254,128.586975 405.897901,128.132611 404.596685,128.132611 L404.596685,128.132611 Z M440.972376,137.281782 C438.686409,146.075934 433.730829,150.834917 426.121547,151.602224 L426.209945,154.121561 L435.093923,154.121561 L434.917127,183.911602 C434.931271,189.004729 435.086851,192.395669 435.447514,194.121547 C436.322652,198.253444 439.020552,200.353591 443.535912,200.353591 C450.068508,200.353591 456.921105,196.374276 464.088398,188.41989 L461.922652,186.563536 C456.747845,191.801819 452.172376,194.430939 448.176796,194.430939 C445.721105,194.430939 444.198895,193.018696 443.624309,190.232044 C443.466961,189.555271 443.403315,188.764471 443.403315,187.845304 L443.491713,154.121561 L457.060773,154.121561 L456.928248,150.099462 L443.535982,150.099462 L443.535982,137.281782 L440.972446,137.281782 L440.972376,137.281782 Z M493.436464,148.508301 C485.84663,148.508301 479.672928,152.192721 474.872928,159.513826 C470.09768,166.847307 468.619669,174.97228 470.497238,183.911602 C471.60221,189.14775 473.803315,193.20593 477.171271,196.066298 C480.533923,198.925436 484.8,200.353591 489.900552,200.353591 C494.649282,200.353591 501.261436,199.151211 504.044199,196.729282 C506.834033,194.308766 509.404641,190.38744 511.779006,185.016575 L509.878453,183.027624 C506.091492,189.995138 498.448619,193.502762 492.685083,193.502762 C484.761105,193.502762 479.908066,189.155359 478.099448,180.508287 C477.864309,179.404545 477.689282,178.218785 477.569061,176.972376 C486.995801,175.479867 494.14011,172.836943 498.961326,169.016575 C503.779006,165.194099 508.616133,161.142283 507.712707,156.861893 C507.175249,154.318328 505.854586,152.318416 503.823204,150.806644 C501.765304,149.295579 496.422541,148.508301 493.436464,148.508301 L493.436464,148.508301 Z M410.475138,148.817694 L394.121547,152.5746 L394.121547,155.491727 L399.779006,154.784545 C402.519337,154.784545 404.131713,156.02548 404.640884,158.497252 C404.812376,159.324485 404.920221,160.486202 404.950276,161.944766 L404.773481,188.685083 C404.727514,192.385414 404.317348,194.536479 403.491713,195.18232 C402.659006,195.829392 400.463204,196.154696 396.906077,196.154696 L396.81768,198.674033 L422.762431,198.674033 L422.718303,196.154696 C419.113441,196.154696 416.776203,195.870239 415.734877,195.314917 C414.711231,194.763145 414.005817,193.758946 413.701728,192.220994 C413.46659,191.112656 413.364049,189.202924 413.348137,186.563536 L413.436535,148.817694 L410.475209,148.817694 L410.475138,148.817694 Z M489.281768,153.76797 C490.860552,153.76797 492.386298,154.377731 493.922652,155.580125 C495.43779,156.778275 496.360663,158.110593 496.662983,159.558025 C498.142762,166.667159 491.84,171.582048 477.657459,174.320442 C477.252597,169.136626 478.150718,164.430865 480.441989,160.17681 C482.71558,155.926814 485.676906,153.76797 489.281768,153.76797 L489.281768,153.76797 Z" fill="#003B57">
                        
                        </path>
                        <path d="M157.887646,9.95179492 L17.1498785,9.95179492 C7.71748066,9.95179492 1.42108547e-14,17.6706899 1.42108547e-14,27.1027341 L1.42108547e-14,182.31016 C1.42108547e-14,191.741666 7.71748066,199.459331 17.1498785,199.459331 L109.843448,199.459331 C108.79135,153.338017 124.54117,63.8308448 157.887646,9.95179492 L157.887646,9.95179492 Z" fill="#0F80CC">
                        
                        </path>
                        <path d="M152.774718,14.9551098 L17.1498785,14.9551098 C10.4523315,14.9551098 5.00207735,20.4039496 5.00207735,27.1027341 L5.00207735,170.986233 C35.7181878,159.197504 81.8193467,149.025535 113.695413,149.487509 C120.100971,115.994079 138.926844,50.3540911 152.774718,14.9551098 L152.774718,14.9551098 Z" fill="url(#linearGradient-1)">
                        
                        </path>
                        <path d="M190.71505,4.8724579 C181.076155,-3.7233432 169.405878,-0.270525525 157.887646,9.95179492 C156.178033,11.470469 154.471956,13.1553308 152.774718,14.9551098 C133.070851,35.8576513 114.781348,74.5758833 109.099138,104.144944 C111.312619,108.633784 113.04168,114.361961 114.180243,118.737651 C114.471956,119.860303 114.735381,120.914005 114.945768,121.810358 C115.446099,123.931729 115.714829,125.307375 115.714829,125.307375 C115.714829,125.307375 115.538033,124.638911 114.813171,122.536988 C114.675271,122.133894 114.521459,121.693673 114.339359,121.175662 C114.261569,120.96174 114.153724,120.70185 114.035271,120.424281 C112.749967,117.436436 109.194608,111.130137 107.629967,108.384502 C106.291624,112.332347 105.108862,116.025607 104.118807,119.367044 C108.635934,127.631883 111.388641,141.795684 111.388641,141.795684 C111.388641,141.795684 111.149967,140.877762 110.014939,137.674056 C109.007204,134.840546 103.987978,126.046381 102.799028,123.990425 C100.765171,131.498587 99.9570387,136.567669 100.68579,137.801872 C102.100685,140.193393 103.448221,144.319802 104.631514,148.88325 C107.304663,159.163729 109.162785,171.678918 109.162785,171.678918 C109.162785,171.678918 109.222895,172.508259 109.323669,173.784553 C108.952398,182.417835 109.17516,191.368811 109.843448,199.459331 C110.729193,210.169253 112.396376,219.369526 114.521459,224.293452 L115.96411,223.506896 C112.843669,213.805939 111.576044,201.092568 112.131182,186.430911 C112.970961,164.020133 118.128088,136.993747 127.65737,108.824723 C143.756376,66.3018502 166.092729,32.1838391 186.535602,15.8903585 C167.903116,32.7177618 142.684994,87.186712 135.135823,107.35732 C126.683227,129.944723 120.693392,151.140929 117.083227,171.4489 C123.311735,152.410321 143.450519,144.226624 143.450519,144.226624 C143.450519,144.226624 153.328088,132.044885 164.871072,114.641298 C157.956597,116.218314 146.602785,118.917983 142.799912,120.516215 C137.190188,122.869364 135.678586,123.672016 135.678586,123.672016 C135.678586,123.672016 153.849635,112.606381 169.43947,107.595994 C190.87947,73.828038 214.237702,25.8563253 190.71505,4.8724579" fill="#003B57">
                        
                        </path>
                        </g>
                    </svg>
                `
        } else if (extension == 'mysql') {
            el.innerHTML = `
                   <svg xmlns="http://www.w3.org/2000/svg" style="transform: scale(1.7)" viewBox="0 0 18.427 4.626"><g fill="#00678c" fill-rule="evenodd"><path d="M2.92 2.906c-.133-.003-.237.01-.324.047-.025.01-.065.01-.068.042.013.013.015.035.027.053a.39.39 0 0 0 .087.102l.107.077c.065.04.138.063.202.103.037.023.073.053.1.078.018.013.03.035.053.043v-.005c-.012-.015-.015-.037-.027-.053l-.05-.048a.79.79 0 0 0-.173-.168c-.053-.037-.17-.087-.192-.148l-.003-.003c.037-.003.08-.017.115-.027.057-.015.108-.012.167-.027l.08-.023v-.015c-.03-.03-.052-.07-.083-.098-.085-.073-.178-.145-.275-.205-.052-.033-.118-.055-.173-.083-.02-.01-.053-.015-.065-.032-.03-.037-.047-.085-.068-.128l-.137-.29c-.03-.065-.048-.13-.085-.19a1.68 1.68 0 0 0-.645-.624c-.062-.035-.135-.05-.213-.068l-.125-.007c-.027-.012-.053-.043-.077-.058-.095-.06-.34-.19-.4-.018-.045.108.067.215.105.27.028.038.065.082.085.125.012.028.015.058.027.088l.087.223a.8.8 0 0 0 .062.103c.013.018.037.027.042.057-.023.033-.025.083-.038.125-.06.188-.037.422.048.56.027.042.1.133.175.098.075-.03.058-.125.08-.208.005-.02.002-.033.012-.047v.003l.068.138c.052.082.142.167.217.223.04.03.072.082.122.1v-.005H1.76c-.01-.015-.025-.022-.038-.033a.81.81 0 0 1-.087-.1 2.15 2.15 0 0 1-.187-.303c-.027-.052-.05-.108-.072-.16-.01-.02-.01-.05-.027-.06-.025.037-.062.068-.08.113-.032.072-.035.16-.047.252-.06-.01-.078-.065-.098-.112-.05-.118-.058-.31-.015-.445.012-.035.062-.145.042-.178-.01-.032-.043-.05-.062-.075-.022-.032-.045-.072-.06-.107C1 1.684.97 1.58.927 1.487.907 1.444.872 1.4.843 1.36.812 1.314.777 1.282.752 1.23.743 1.21.732 1.18.745 1.16c.003-.013.01-.018.023-.022.022-.018.083.005.105.015.062.025.113.048.165.083.023.017.048.048.078.057h.035c.053.012.113.003.163.018.088.028.168.07.24.115a1.48 1.48 0 0 1 .52.57c.02.038.028.073.047.113l.113.245c.035.078.068.158.118.223.025.035.125.053.17.072.033.015.085.028.115.047l.167.113c.027.02.1.062.115.095z"/><path d="M1.22 1.457c-.028 0-.048.003-.068.008v.003h.003c.013.027.037.045.053.068l.038.08.003-.003c.023-.017.035-.043.035-.083-.01-.012-.012-.023-.02-.035-.01-.017-.032-.025-.045-.038z"/></g><path d="M10.064 3.34h1.434c.168 0 .328-.034.458-.095.217-.1.32-.233.32-.408v-.366c0-.14-.118-.275-.354-.366a1.25 1.25 0 0 0-.423-.072h-.602c-.202 0-.297-.06-.324-.194-.004-.015-.004-.03-.004-.046v-.225c0-.012 0-.027.004-.042.027-.103.08-.13.256-.15h1.468v-.332H10.9c-.202 0-.31.012-.404.042-.294.09-.423.236-.423.492v.29c0 .225.252.416.68.46.046.004.095.004.145.004h.515c.02 0 .038 0 .053.004.156.015.225.042.27.1.03.03.038.057.038.092v.29c0 .034-.023.08-.07.118s-.118.065-.214.07c-.02 0-.03.004-.05.004h-1.376zm5.315-.576c0 .34.256.53.767.568l.145.008h1.296V3.01H16.28c-.3 0-.4-.072-.4-.248V1.045h-.5v1.72zm-2.787.015V1.598c0-.3.213-.484.63-.54l.133-.008h.946c.05 0 .092.004.14.008.416.057.625.24.625.54V2.78c0 .244-.088.374-.294.46l.488.442h-.576l-.397-.358-.4.023h-.534c-.088 0-.187-.01-.3-.038-.316-.088-.473-.256-.473-.53zm.538-.026c0 .015.008.03.012.05.027.137.156.213.354.213h.45l-.412-.374h.576l.362.328c.07-.038.11-.092.126-.16.004-.015.004-.034.004-.05V1.63c0-.015 0-.03-.004-.046-.027-.13-.156-.202-.35-.202h-.75c-.22 0-.366.095-.366.248z" fill="#ce8b2c" fill-rule="evenodd"/><path d="M3.445 3.342h.496V1.378l.774 1.712c.088.206.214.282.458.282s.362-.076.454-.282l.77-1.712v1.964h.5V1.378c0-.19-.076-.282-.236-.332-.377-.114-.63-.015-.744.24l-.76 1.693-.732-1.693c-.11-.255-.366-.354-.747-.24-.156.05-.233.14-.233.332v1.964zm3.863-1.598h.5v1.08c-.004.06.02.198.3.202H9.18v-1.29h.5v1.765c0 .435-.538.53-.79.534H7.32v-.332h1.575c.32-.034.282-.194.282-.248v-.13H8.12c-.492-.004-.808-.22-.812-.47V1.744z" fill="#00678c" fill-rule="evenodd"/></svg>
                `
        }
        else if (extension == 'postgresql') {
            el.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" style="transform: scale(.9)" viewBox="-4 0 264 264" preserveAspectRatio="xMinYMin meet"><path d="M255.008 158.086c-1.535-4.649-5.556-7.887-10.756-8.664-2.452-.366-5.26-.21-8.583.475-5.792 1.195-10.089 1.65-13.225 1.738 11.837-19.985 21.462-42.775 27.003-64.228 8.96-34.689 4.172-50.492-1.423-57.64C233.217 10.847 211.614.683 185.552.372c-13.903-.17-26.108 2.575-32.475 4.549-5.928-1.046-12.302-1.63-18.99-1.738-12.537-.2-23.614 2.533-33.079 8.15-5.24-1.772-13.65-4.27-23.362-5.864-22.842-3.75-41.252-.828-54.718 8.685C6.622 25.672-.937 45.684.461 73.634c.444 8.874 5.408 35.874 13.224 61.48 4.492 14.718 9.282 26.94 14.237 36.33 7.027 13.315 14.546 21.156 22.987 23.972 4.731 1.576 13.327 2.68 22.368-4.85 1.146 1.388 2.675 2.767 4.704 4.048 2.577 1.625 5.728 2.953 8.875 3.74 11.341 2.835 21.964 2.126 31.027-1.848.056 1.612.099 3.152.135 4.482.06 2.157.12 4.272.199 6.25.537 13.374 1.447 23.773 4.143 31.049.148.4.347 1.01.557 1.657 1.345 4.118 3.594 11.012 9.316 16.411 5.925 5.593 13.092 7.308 19.656 7.308 3.292 0 6.433-.432 9.188-1.022 9.82-2.105 20.973-5.311 29.041-16.799 7.628-10.86 11.336-27.217 12.007-52.99.087-.729.167-1.425.244-2.088l.16-1.362 1.797.158.463.031c10.002.456 22.232-1.665 29.743-5.154 5.935-2.754 24.954-12.795 20.476-26.351"/><path d="M237.906 160.722c-29.74 6.135-31.785-3.934-31.785-3.934 31.4-46.593 44.527-105.736 33.2-120.211-30.904-39.485-84.399-20.811-85.292-20.327l-.287.052c-5.876-1.22-12.451-1.946-19.842-2.067-13.456-.22-23.664 3.528-31.41 9.402 0 0-95.43-39.314-90.991 49.444.944 18.882 27.064 142.873 58.218 105.422 11.387-13.695 22.39-25.274 22.39-25.274 5.464 3.63 12.006 5.482 18.864 4.817l.533-.452c-.166 1.7-.09 3.363.213 5.332-8.026 8.967-5.667 10.541-21.711 13.844-16.235 3.346-6.698 9.302-.471 10.86 7.549 1.887 25.013 4.561 36.813-11.958l-.47 1.885c3.144 2.519 5.352 16.383 4.982 28.952-.37 12.568-.617 21.197 1.86 27.937 2.479 6.74 4.948 21.905 26.04 17.386 17.623-3.777 26.756-13.564 28.027-29.89.901-11.606 2.942-9.89 3.07-20.267l1.637-4.912c1.887-15.733.3-20.809 11.157-18.448l2.64.232c7.99.363 18.45-1.286 24.589-4.139 13.218-6.134 21.058-16.377 8.024-13.686h.002" fill="#336791"/><path d="M108.076 81.525c-2.68-.373-5.107-.028-6.335.902-.69.523-.904 1.129-.962 1.546-.154 1.105.62 2.327 1.096 2.957 1.346 1.784 3.312 3.01 5.258 3.28.282.04.563.058.842.058 3.245 0 6.196-2.527 6.456-4.392.325-2.336-3.066-3.893-6.355-4.35M196.86 81.599c-.256-1.831-3.514-2.353-6.606-1.923-3.088.43-6.082 1.824-5.832 3.659.2 1.427 2.777 3.863 5.827 3.863.258 0 .518-.017.78-.054 2.036-.282 3.53-1.575 4.24-2.32 1.08-1.136 1.706-2.402 1.591-3.225" fill="#FFF"/><path d="M247.802 160.025c-1.134-3.429-4.784-4.532-10.848-3.28-18.005 3.716-24.453 1.142-26.57-.417 13.995-21.32 25.508-47.092 31.719-71.137 2.942-11.39 4.567-21.968 4.7-30.59.147-9.463-1.465-16.417-4.789-20.665-13.402-17.125-33.072-26.311-56.882-26.563-16.369-.184-30.199 4.005-32.88 5.183-5.646-1.404-11.801-2.266-18.502-2.376-12.288-.199-22.91 2.743-31.704 8.74-3.82-1.422-13.692-4.811-25.765-6.756-20.872-3.36-37.458-.814-49.294 7.571-14.123 10.006-20.643 27.892-19.38 53.16.425 8.501 5.269 34.653 12.913 59.698 10.062 32.964 21 51.625 32.508 55.464 1.347.449 2.9.763 4.613.763 4.198 0 9.345-1.892 14.7-8.33a529.832 529.832 0 0 1 20.261-22.926c4.524 2.428 9.494 3.784 14.577 3.92.01.133.023.266.035.398a117.66 117.66 0 0 0-2.57 3.175c-3.522 4.471-4.255 5.402-15.592 7.736-3.225.666-11.79 2.431-11.916 8.435-.136 6.56 10.125 9.315 11.294 9.607 4.074 1.02 7.999 1.523 11.742 1.523 9.103 0 17.114-2.992 23.516-8.781-.197 23.386.778 46.43 3.586 53.451 2.3 5.748 7.918 19.795 25.664 19.794 2.604 0 5.47-.303 8.623-.979 18.521-3.97 26.564-12.156 29.675-30.203 1.665-9.645 4.522-32.676 5.866-45.03 2.836.885 6.487 1.29 10.434 1.289 8.232 0 17.731-1.749 23.688-4.514 6.692-3.108 18.768-10.734 16.578-17.36zm-44.106-83.48c-.061 3.647-.563 6.958-1.095 10.414-.573 3.717-1.165 7.56-1.314 12.225-.147 4.54.42 9.26.968 13.825 1.108 9.22 2.245 18.712-2.156 28.078a36.508 36.508 0 0 1-1.95-4.009c-.547-1.326-1.735-3.456-3.38-6.404-6.399-11.476-21.384-38.35-13.713-49.316 2.285-3.264 8.084-6.62 22.64-4.813zm-17.644-61.787c21.334.471 38.21 8.452 50.158 23.72 9.164 11.711-.927 64.998-30.14 110.969a171.33 171.33 0 0 0-.886-1.117l-.37-.462c7.549-12.467 6.073-24.802 4.759-35.738-.54-4.488-1.05-8.727-.92-12.709.134-4.22.692-7.84 1.232-11.34.663-4.313 1.338-8.776 1.152-14.037.139-.552.195-1.204.122-1.978-.475-5.045-6.235-20.144-17.975-33.81-6.422-7.475-15.787-15.84-28.574-21.482 5.5-1.14 13.021-2.203 21.442-2.016zM66.674 175.778c-5.9 7.094-9.974 5.734-11.314 5.288-8.73-2.912-18.86-21.364-27.791-50.624-7.728-25.318-12.244-50.777-12.602-57.916-1.128-22.578 4.345-38.313 16.268-46.769 19.404-13.76 51.306-5.524 64.125-1.347-.184.182-.376.352-.558.537-21.036 21.244-20.537 57.54-20.485 59.759-.002.856.07 2.068.168 3.735.362 6.105 1.036 17.467-.764 30.334-1.672 11.957 2.014 23.66 10.111 32.109a36.275 36.275 0 0 0 2.617 2.468c-3.604 3.86-11.437 12.396-19.775 22.426zm22.479-29.993c-6.526-6.81-9.49-16.282-8.133-25.99 1.9-13.592 1.199-25.43.822-31.79-.053-.89-.1-1.67-.127-2.285 3.073-2.725 17.314-10.355 27.47-8.028 4.634 1.061 7.458 4.217 8.632 9.645 6.076 28.103.804 39.816-3.432 49.229-.873 1.939-1.698 3.772-2.402 5.668l-.546 1.466c-1.382 3.706-2.668 7.152-3.465 10.424-6.938-.02-13.687-2.984-18.819-8.34zm1.065 37.9c-2.026-.506-3.848-1.385-4.917-2.114.893-.42 2.482-.992 5.238-1.56 13.337-2.745 15.397-4.683 19.895-10.394 1.031-1.31 2.2-2.794 3.819-4.602l.002-.002c2.411-2.7 3.514-2.242 5.514-1.412 1.621.67 3.2 2.702 3.84 4.938.303 1.056.643 3.06-.47 4.62-9.396 13.156-23.088 12.987-32.921 10.526zm69.799 64.952c-16.316 3.496-22.093-4.829-25.9-14.346-2.457-6.144-3.665-33.85-2.808-64.447.011-.407-.047-.8-.159-1.17a15.444 15.444 0 0 0-.456-2.162c-1.274-4.452-4.379-8.176-8.104-9.72-1.48-.613-4.196-1.738-7.46-.903.696-2.868 1.903-6.107 3.212-9.614l.549-1.475c.618-1.663 1.394-3.386 2.214-5.21 4.433-9.848 10.504-23.337 3.915-53.81-2.468-11.414-10.71-16.988-23.204-15.693-7.49.775-14.343 3.797-17.761 5.53-.735.372-1.407.732-2.035 1.082.954-11.5 4.558-32.992 18.04-46.59 8.489-8.56 19.794-12.788 33.568-12.56 27.14.444 44.544 14.372 54.366 25.979 8.464 10.001 13.047 20.076 14.876 25.51-13.755-1.399-23.11 1.316-27.852 8.096-10.317 14.748 5.644 43.372 13.315 57.129 1.407 2.521 2.621 4.7 3.003 5.626 2.498 6.054 5.732 10.096 8.093 13.046.724.904 1.426 1.781 1.96 2.547-4.166 1.201-11.649 3.976-10.967 17.847-.55 6.96-4.461 39.546-6.448 51.059-2.623 15.21-8.22 20.875-23.957 24.25zm68.104-77.936c-4.26 1.977-11.389 3.46-18.161 3.779-7.48.35-11.288-.838-12.184-1.569-.42-8.644 2.797-9.547 6.202-10.503.535-.15 1.057-.297 1.561-.473.313.255.656.508 1.032.756 6.012 3.968 16.735 4.396 31.874 1.271l.166-.033c-2.042 1.909-5.536 4.471-10.49 6.772z" fill="#FFF"/></svg>
            `
        } else if (extension != '.zip') {
            el.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" style="transform: scale(1.3)">
                        <path d="M49,61H23a5.0147,5.0147,0,0,1-5-5V16a5.0147,5.0147,0,0,1,5-5H40.9091L54,22.1111V56A5.0147,5.0147,0,0,1,49,61Z" style="fill: #e3edfc;"></path>
                        <path d="M54,22.1111H44.1818a3.3034,3.3034,0,0,1-3.2727-3.3333V11s1.8409.2083,6.9545,4.5833C52.8409,20.0972,54,22.1111,54,22.1111Z" style="fill: #b7d0ea;"></path>
                        <path d="M19.03,59A4.9835,4.9835,0,0,0,23,61H49a4.9835,4.9835,0,0,0,3.97-2Z" style="fill: #c4dbf2;"></path>
                        <rect x="27" y="31" width="18" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                        <rect x="27" y="35" width="18" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                        <rect x="27" y="39" width="18" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                        <rect x="27" y="43" width="14" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                        <rect x="27" y="47" width="8" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                    </svg>
                `
        } else {
            el.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" style="transform: scale(1.3)">
                            <g>
                                <rect x="18" y="16" width="36" height="40" rx="5" ry="5" style="fill: #e3edfc;"></rect>
                                <path d="M19.03,54A4.9835,4.9835,0,0,0,23,56H49a4.9835,4.9835,0,0,0,3.97-2Z" style="fill: #c4dbf2;"></path>
                                <rect x="32" y="20" width="8" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                                <rect x="32" y="25" width="8" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                                <rect x="32" y="30" width="8" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                                <rect x="32" y="35" width="8" height="2" rx="1" ry="1" style="fill: #7e95c4;"></rect>
                                <path d="M35,16.0594h2a0,0,0,0,1,0,0V41a1,1,0,0,1-1,1h0a1,1,0,0,1-1-1V16.0594A0,0,0,0,1,35,16.0594Z" style="fill: #7e95c4;"></path>
                                <path d="M38.0024,40H33.9976A1.9976,1.9976,0,0,0,32,41.9976v2.0047A1.9976,1.9976,0,0,0,33.9976,46h4.0047A1.9976,1.9976,0,0,0,40,44.0024V41.9976A1.9976,1.9976,0,0,0,38.0024,40Zm-.0053,4H34V42h4Z" style="fill: #7e95c4;"></path>
                            </g>
                        </svg>
                    `
        }
    })
}

setFileIcons()