"use strict";

(function (NioApp, $) {
  'use strict';

  // Uses
  // NioApp.Toast(message, type, {attr});
  //
  // @message     = 'Your message'
  // @type        = 'info|success|warning|error',
  // @attr        = {position: 'bottom-right', icon: 'auto', ui: ''}
  //
  // attr.ui used for additonal class as is-dark
  // attr.icon used for custom icon
  // attr.position used for position of the msg.

  // Example Trigger
  $('.eg-toastr-default').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پیش فرض پیام toast است.', 'info');
  });
  $('.eg-toastr-bottom-center').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پایین وسط پیام toast است.', 'info', {
      position: 'bottom-center'
    });
  });
  $('.eg-toastr-bottom-left').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پایین سمت چپ پیام toast است.', 'info');
  });
  $('.eg-toastr-bottom-right').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پایین سمت راست پیام toast است.', 'info', {
      position: 'bottom-left'
    });
  });
  $('.eg-toastr-bottom-full').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای تمام عرض پایین پیام toast است.', 'info', {
      position: 'bottom-full'
    });
  });
  $('.eg-toastr-top-center').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای بالا وسط پیام toast است.', 'info', {
      position: 'top-center'
    });
  });
  $('.eg-toastr-top-left').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای بالا سمت چپ پیام toast است.', 'info', {
      position: 'top-right'
    });
  });
  $('.eg-toastr-top-right').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای بالا سمت راست پیام toast است.', 'info', {
      position: 'top-left'
    });
  });
  $('.eg-toastr-top-full').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای تمام عرض بالا پیام toast است.', 'info', {
      position: 'top-full'
    });
  });
  $('.eg-toastr-info').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پایین سمت چپ پیام toast است.', 'info');
  });
  $('.eg-toastr-success').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پیام موفقیت آمیز toast است.', 'success');
  });
  $('.eg-toastr-warning').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پیام هشدار toast است.', 'warning');
  });
  $('.eg-toastr-error').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این یک نکته برای پیام خطای toast است.', 'error');
  });
  $('.eg-toastr-dark').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این نکته نسخه تاریک پیام toast است.', 'info', {
      ui: 'is-dark'
    });
  });
  $('.eg-toastr-no-icon').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('این نکته بدون آیکون پیام toast است.', 'info', {
      icon: false
    });
  });
  $('.eg-toastr-with-title').on("click", function (e) {
    e.preventDefault();
    toastr.clear();
    NioApp.Toast('<h5>به روز رسانی موفقیت آمیز</h5><p>پروفایل شما با موفقیت به روز رسانی شد.</p>', 'success');
  });
})(NioApp, jQuery);