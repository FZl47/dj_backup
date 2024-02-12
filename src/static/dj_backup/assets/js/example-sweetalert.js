"use strict";

(function (NioApp, $) {
  'use strict';

  // Basic Sweet Alerts
  $('.eg-swal-default').on("click", function (e) {
    Swal.fire('یک محتوای  Sweet Alert ساده');
    e.preventDefault();
  });
  $('.eg-swal-default-s2').on("click", function (e) {
    Swal.fire('اینترنت؟', 'آن چیز هنوز در اطراف است؟');
    e.preventDefault();
  });
  $('.eg-swal-success').on("click", function (e) {
    Swal.fire("آفرین!", "شما روی دکمه کلیک کردید!", "success");
    e.preventDefault();
  });
  $('.eg-swal-info').on("click", function (e) {
    Swal.fire("آفرین!", "شما روی دکمه کلیک کردید!", "info");
    e.preventDefault();
  });
  $('.eg-swal-warning').on("click", function (e) {
    Swal.fire("آفرین!", "شما روی دکمه کلیک کردید!", "warning");
    e.preventDefault();
  });
  $('.eg-swal-error').on("click", function (e) {
    Swal.fire("آفرین!", "شما روی دکمه کلیک کردید!", "error");
    e.preventDefault();
  });
  $('.eg-swal-question').on("click", function (e) {
    Swal.fire("آفرین!", "شما روی دکمه کلیک کردید!", "question");
    e.preventDefault();
  });

  // Advanced Sweet Alerts
  $('.eg-swal-av1').on("click", function (e) {
    Swal.fire({
      icon: 'error',
      title: 'اوه...',
      text: 'مشکلی پیش آمد!',
      footer: '<a href>چرا من این مشکل را دارم؟</a>'
    });
    e.preventDefault();
  });
  $('.eg-swal-av2').on("click", function (e) {
    Swal.fire({
      title: '<strong><u>مثال</u> HTML</strong>',
      icon: 'info',
      html: 'می توانید از <b>متن پررنگ</b>، ' + '<a href="//sweetalert2.github.io">لینک ها</a> ' + 'و سایر تگ های HTML استفاده کنید',
      showCloseButton: true,
      showCancelButton: true,
      focusConfirm: false,
      confirmButtonText: '<i class="fa fa-thumbs-up"></i> عالی!',
      confirmButtonAriaLabel: 'دمت گرم، عالی!',
      cancelButtonText: '<i class="fa fa-thumbs-down"></i>',
      cancelButtonAriaLabel: 'گند زدی'
    });
    e.preventDefault();
  });
  $('.eg-swal-av2').on("click", function (e) {
    Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: 'کار شما ذخیره شد',
      showConfirmButton: false,
      timer: 1500
    });
    e.preventDefault();
  });
  $('.eg-swal-av3').on("click", function (e) {
    Swal.fire({
      title: 'مطمئن هستید؟',
      text: "شما نمی توانید این را برگردانید!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'بله حذف شود!'
    }).then(function (result) {
      if (result.value) {
        Swal.fire('حذف شد!', 'فایل شما حذف شد', 'success');
      }
    });
    e.preventDefault();
  });
  $('.eg-swal-av4').on("click", function (e) {
    Swal.fire({
      title: 'دلنشین!',
      text: 'مودال با تصویر سفارشی.',
      imageUrl: 'https://unsplash.it/400/200',
      imageWidth: 400,
      imageHeight: 200,
      imageAlt: 'تصویر سفارشی'
    });
    e.preventDefault();
  });
  $('.eg-swal-av5').on("click", function (e) {
    var timerInterval;
    Swal.fire({
      title: 'هشدار با بسته شدن خودکار!',
      html: 'من در <b></b> میلی ثانیه بسته می شوم.',
      timer: 2000,
      timerProgressBar: true,
      onBeforeOpen: function onBeforeOpen() {
        Swal.showLoading();
        timerInterval = setInterval(function () {
          Swal.getContent().querySelector('b').textContent = Swal.getTimerLeft();
        }, 100);
      },
      onClose: function onClose() {
        clearInterval(timerInterval);
      }
    }).then(function (result) {
      if ( /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.timer) {
        console.log('I was closed by the timer'); // eslint-disable-line
      }
    });

    e.preventDefault();
  });
  $('.eg-swal-av6').on("click", function (e) {
    Swal.fire({
      title: 'نام کاربری گیت هاب خود را ارسال کنید',
      input: 'text',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      confirmButtonText: 'جستجو',
      showLoaderOnConfirm: true,
      preConfirm: function preConfirm(login) {
        return fetch("//api.github.com/users/".concat(login)).then(function (response) {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        })["catch"](function (error) {
          Swal.showValidationMessage("درخواست ناموفق بود: ".concat(error));
        });
      },
      allowOutsideClick: function allowOutsideClick() {
        return !Swal.isLoading();
      }
    }).then(function (result) {
      if (result.value) {
        Swal.fire({
          title: "".concat("آواتار", result.value.login),
          imageUrl: result.value.avatar_url,
          imageWidth: '120px'
        });
      }
    });
    e.preventDefault();
  });
})(NioApp, jQuery);