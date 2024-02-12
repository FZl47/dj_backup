"use strict";

!function (NioApp, $) {
  "use strict";

  //////// for developer - barchart ////////
  // Avilable options to pass from outside
  // labels: array,
  // stacked: false - boolean,
  // legend: false - boolean,
  // dataUnit: string, (Used in tooltip or other section for display)
  // datasets: [{label : string, color: string (color code with # or other format), data: array}]
  var barChartData = {
    labels: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"],
    dataUnit: 'نفر',
    datasets: [{
      label: "عضو",
      color: "#b695ff",
      data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 75, 90]
    }]
  };
  var barChartMultiple = {
    labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    dataUnit: 'تومان',
    datasets: [{
      label: "درآمد",
      color: "#b695ff",
      data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95]
    }, {
      label: "هزینه",
      color: "#f4aaa4",
      data: [75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125]
    }]
  };
  var barChartStacked = {
    labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    stacked: true,
    dataUnit: 'تومان',
    datasets: [{
      label: "درآمد",
      color: "#b695ff",
      data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95]
    }, {
      label: "هزینه",
      color: "#f4aaa4",
      data: [75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125]
    }]
  };
  function barChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.bar-chart');
    $selector.each(function () {
      var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data,
        _d_legend = typeof _get_data.legend === 'undefined' ? false : _get_data.legend;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          label: _get_data.datasets[i].label,
          data: _get_data.datasets[i].data,
          // Styles
          backgroundColor: _get_data.datasets[i].color,
          borderWidth: 2,
          borderColor: 'transparent',
          hoverBorderColor: 'transparent',
          borderSkipped: 'bottom',
          barPercentage: NioApp.State.asMobile ? .95 : .75,
          categoryPercentage: NioApp.State.asMobile ? .95 : .75
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'bar',
        data: {
          labels: _get_data.labels,
          datasets: chart_data
        },
        options: {
          plugins: {
            legend: {
              display: _get_data.legend ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 30,
                padding: 20,
                color: '#6783b8'
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function label(context) {
                  return "".concat(context.parsed.y, " ").concat(_get_data.dataUnit);
                }
              },
              backgroundColor: '#eff6ff',
              titleFont: {
                size: 13
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            }
          },
          maintainAspectRatio: false,
          scales: {
            y: {
              display: true,
              stacked: _get_data.stacked ? _get_data.stacked : false,
              position: NioApp.State.isRTL ? "right" : "left",
              ticks: {
                beginAtZero: true,
                font: {
                  size: 12
                },
                color: '#9eaecf'
              },
              grid: {
                color: NioApp.hexRGB("#526484", .2),
                tickLength: 0,
                zeroLineColor: NioApp.hexRGB("#526484", .2),
                drawTicks: false
              }
            },
            x: {
              display: true,
              stacked: _get_data.stacked ? _get_data.stacked : false,
              ticks: {
                font: {
                  size: 12
                },
                color: '#9eaecf',
                source: 'auto',
                reverse: NioApp.State.isRTL
              },
              grid: {
                color: "transparent",
                tickLength: 10,
                zeroLineColor: 'transparent',
                drawTicks: false
              }
            }
          }
        }
      });
    });
  }
  // init bar chart
  barChart();

  //////// for developer - linechart ////////
  // Avilable options to pass from outside
  // labels: array,
  // legend: false - boolean,
  // dataUnit: string, (Used in tooltip or other section for display)
  // datasets: [{label : string, color: string (color code with # or other format), data: array}]
  var solidLineChart = {
    labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    dataUnit: 'بیت کوین',
    lineTension: .4,
    legend: true,
    datasets: [{
      label: "مجموع دریافت شده",
      color: "#5ce0aa",
      background: 'transparent',
      data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95]
    }, {
      label: "مجموع ارسال",
      color: "#9d72ff",
      background: 'transparent',
      data: [80, 54, 105, 120, 82, 85, 60, 80, 54, 105, 120, 82]
    }]
  };
  var filledLineChart = {
    labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    dataUnit: 'بیت کوین',
    lineTension: .4,
    datasets: [{
      label: "مجموع دریافت شده",
      color: "#9d72ff",
      background: NioApp.hexRGB('#9d72ff', .4),
      data: [110, 80, 125, 65, 95, 75, 90, 110, 80, 125, 70, 95]
    }]
  };
  var straightLineChart = {
    labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    dataUnit: 'بیت کوین',
    lineTension: 0,
    datasets: [{
      label: "مجموع دریافت شده",
      color: "#9d72ff",
      background: NioApp.hexRGB('#9d72ff', .3),
      data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95]
    }]
  };
  function lineChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.line-chart');
    $selector.each(function () {
      var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          label: _get_data.datasets[i].label,
          tension: _get_data.lineTension,
          backgroundColor: _get_data.datasets[i].background,
          fill: true,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].color,
          pointBorderColor: _get_data.datasets[i].color,
          pointBackgroundColor: '#fff',
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: _get_data.datasets[i].color,
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 2,
          pointRadius: 4,
          pointHitRadius: 4,
          data: _get_data.datasets[i].data
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'line',
        data: {
          labels: _get_data.labels,
          datasets: chart_data
        },
        options: {
          plugins: {
            legend: {
              display: _get_data.legend ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 12,
                padding: 20,
                color: '#6783b8'
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function label(context) {
                  return "".concat(context.parsed.y, " ").concat(_get_data.dataUnit);
                }
              },
              backgroundColor: '#eff6ff',
              titleFont: {
                size: 13
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            }
          },
          maintainAspectRatio: false,
          scales: {
            y: {
              display: true,
              position: NioApp.State.isRTL ? "right" : "left",
              ticks: {
                beginAtZero: false,
                font: {
                  size: 12
                },
                color: '#9eaecf',
                padding: 10
              },
              grid: {
                color: NioApp.hexRGB("#526484", .2),
                tickLength: 0,
                zeroLineColor: NioApp.hexRGB("#526484", .2),
                drawTicks: false
              }
            },
            x: {
              display: true,
              ticks: {
                font: {
                  size: 12
                },
                color: '#9eaecf',
                source: 'auto',
                padding: 5,
                reverse: NioApp.State.isRTL
              },
              grid: {
                color: "transparent",
                tickLength: 10,
                zeroLineColor: NioApp.hexRGB("#526484", .2),
                offset: true,
                drawTicks: false
              }
            }
          }
        }
      });
    });
  }

  // init line chart
  lineChart();

  //////// for developer - pieChart ////////
  // Avilable options to pass from outside
  // labels: array,
  // legend: false - boolean,
  // dataUnit: string, (Used in tooltip or other section for display)
  // datasets: [{label : string, color: string (color code with # or other format), data: array}]
  var pieChartData = {
    labels: ["ارسال", "دریافت", "برداشت"],
    dataUnit: 'بیت کوین',
    legend: false,
    datasets: [{
      borderColor: "#fff",
      background: ["#b695ff", "#f4aaa4", "#8feac5"],
      data: [110, 80, 125]
    }]
  };
  function pieChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.pie-chart');
    $selector.each(function () {
      var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          backgroundColor: _get_data.datasets[i].background,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].borderColor,
          hoverBorderColor: _get_data.datasets[i].borderColor,
          data: _get_data.datasets[i].data
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'pie',
        data: {
          labels: _get_data.labels,
          datasets: chart_data
        },
        options: {
          plugins: {
            legend: {
              display: _get_data.legend ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 12,
                padding: 20,
                color: '#6783b8'
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function label(context) {
                  return "".concat(context.parsed, " ").concat(_get_data.dataUnit);
                }
              },
              backgroundColor: '#eff6ff',
              titleFont: {
                size: 13
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            }
          },
          rotation: -.2,
          maintainAspectRatio: false
        }
      });
    });
  }

  // init pie chart
  pieChart();
  var doughnutChartData = {
    labels: ["ارسال", "دریافت", "برداشت"],
    dataUnit: 'بیت کوین',
    legend: false,
    datasets: [{
      borderColor: "#fff",
      background: ["#b695ff", "#f4aaa4", "#8feac5"],
      data: [110, 80, 125]
    }]
  };
  function doughnutChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.doughnut-chart');
    $selector.each(function () {
      var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          backgroundColor: _get_data.datasets[i].background,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].borderColor,
          hoverBorderColor: _get_data.datasets[i].borderColor,
          data: _get_data.datasets[i].data
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'doughnut',
        data: {
          labels: _get_data.labels,
          datasets: chart_data
        },
        options: {
          plugins: {
            legend: {
              display: _get_data.legend ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 12,
                padding: 20,
                color: '#6783b8'
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function label(context) {
                  return "".concat(context.parsed, " ").concat(_get_data.dataUnit);
                }
              },
              backgroundColor: '#eff6ff',
              titleFont: {
                size: 13
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            }
          },
          rotation: 1,
          cutoutPercentage: 40,
          maintainAspectRatio: false
        }
      });
    });
  }

  // init doughnut chart
  doughnutChart();
  var polarChartData = {
    labels: ["ارسال", "دریافت", "برداشت"],
    dataUnit: 'بیت کوین',
    legend: false,
    datasets: [{
      borderColor: "#fff",
      background: [NioApp.hexRGB("#b695ff", .8), NioApp.hexRGB("#f4aaa4", .8), NioApp.hexRGB("#8feac5", .8)],
      data: [110, 80, 125]
    }]
  };
  function polarAreaChart(selector, set_data) {
    var $selector = selector ? $(selector) : $('.polar-chart');
    $selector.each(function () {
      var $self = $(this),
        _self_id = $self.attr('id'),
        _get_data = typeof set_data === 'undefined' ? eval(_self_id) : set_data;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");
      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          backgroundColor: _get_data.datasets[i].background,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].borderColor,
          hoverBorderColor: _get_data.datasets[i].borderColor,
          data: _get_data.datasets[i].data
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'polarArea',
        data: {
          labels: _get_data.labels,
          datasets: chart_data
        },
        options: {
          plugins: {
            legend: {
              display: _get_data.legend ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 12,
                padding: 20,
                color: '#6783b8'
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function label(context) {
                  return "".concat(context.parsed.r, " ").concat(_get_data.dataUnit);
                }
              },
              backgroundColor: '#eff6ff',
              titleFont: {
                size: 13
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            }
          },
          maintainAspectRatio: false
        }
      });
    });
  }

  // init line chart
  polarAreaChart();
}(NioApp, jQuery);