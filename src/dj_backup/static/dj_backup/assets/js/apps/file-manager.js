"use strict";

!function (NioApp, $) {
  "use strict";

  var $win = $(window),
    $body = $('body'),
    breaks = NioApp.Break;

  // Variable
  var $file_dload = $('.file-dl-toast');
  NioApp.FileManager = function () {
    $file_dload.on("click", function (e) {
      e.preventDefault();
      NioApp.Toast('<h5>در حال دانلود فایل</h5><p>در حال تولید فایل برای شروع دانلود.</p>', 'success', {
        position: 'bottom-center',
        icon: 'ni ni-download-cloud',
        ui: 'is-dark'
      });
    });
  };
  NioApp.coms.docReady.push(NioApp.FileManager);
}(NioApp, jQuery);