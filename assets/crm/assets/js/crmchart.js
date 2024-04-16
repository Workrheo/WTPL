// Revenue VS Expense Chart
var options = {
    series: [totalRevenue, totalExpense],
    chart: {
      type: 'donut',
      height: '200',
      width: '180',  // set the width of the chart here
    },
    labels: ['Revenue', 'Expense'],
    colors: ['#5d65cf', 'rgba(255, 99, 132, 0.8)'],
    dataLabels: {
      enabled: false,
    },
    legend: {
      position: 'bottom',
      fontSize: '12px',
      fontWeight: 'bold',
      labels: {
        colors: '#919090' // Set the legend label color to white
      }
    },
    tooltip: {
      y: {
        formatter: function (value) {
          return value.toLocaleString();
        },
      },
    },
    responsive: [{
      breakpoint: 480,
      options: {
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom'
        }
      }
    }]
  };
  
  var chart = new ApexCharts(document.querySelector("#revenueExpenseChart"), options);
  chart.render();


// Invoice Chart
var optionsPie = {
  series: [paidInvoice, unpaidInvoice],
  chart: {
    type: 'pie',
  },
  labels: ['Paid', 'Unpaid'],
  colors: ['#7B68EE', '#FF6347'],
  dataLabels: {
    enabled: false,
  },
  legend: {
    position: 'bottom',
    fontSize: '12px',
    fontWeight: 'bold',
    labels: {
      colors: '#919090' // Set the legend label color to white
    }
  },
  tooltip: {
    y: {
      formatter: function (value) {
        return value.toLocaleString();
      },
    },
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {},
      legend: {
        position: 'bottom'
      }
    }
  }]
};

var chartPie = new ApexCharts(document.querySelector("#invoiceStatusChart"), optionsPie);
chartPie.render();

// Widget Invoice
var optionsDonut = {
  series: [paidInvoice, unpaidInvoice, overdueInvoice],
  chart: {
    type: 'donut', // Set the chart type as 'donut'
    width : '150',
    height : '200'
  },
  labels: ['Paid', 'Unpaid', 'Overdue'],
  colors: ['#8140d6', '#ebbd34', '#d64040'],
  dataLabels: {
    enabled: false,
  },
  legend: {
    position: 'bottom',
    fontSize: '12px',
    fontWeight: 'bold',
    labels: {
      colors: '#919090' // Set the legend label color to white
    }
  },
  tooltip: {
    y: {
      formatter: function (value) {
        return value.toLocaleString();
      },
    },
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {},
      legend: {
        position: 'bottom'
      }
    }
  }]
};

var chartDonut = new ApexCharts(document.querySelector("#invoiceWidgetChart"), optionsDonut);
chartDonut.render();


// Task Chart
var options = {
    series: [toDoCount, inProgressCount, doneCount],
    chart: {
        width: 300,
        height: 200,
        type: 'donut',
        toolbar: {
          show: false
        }
    },
    labels: ['To Do', 'In Progress', 'Done'],
    colors: ['#FF3B30', '#FFCC00', '#007AFF'],
    legend: {
      show: false  // Set show property to false to hide the legend
    },
    dataLabels: {
        enabled: false
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }],
    tooltip: {
        y: {
            formatter: function(val) {
                return val.toLocaleString();
            }
        }
    }
}

var chart = new ApexCharts(document.querySelector("#taskStatusChart"), options);
chart.render();

// Profit Chart
var options = {
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false
    },
    width: '100%',
  },
  dataLabels: {
    enabled: false
  },
  series: [{
    name: 'Profit',
    data: [profit * 0.8, profit * 0.9, profit]
  }],
  colors: ['#198754'],
  stroke: {
    show: true,
    curve: 'smooth',
    lineCap: 'butt',
    colors: ['#79c280'], // Stroke gradient colors
    width: 3, // Make lines a bit thicker
    dashArray: 0,
  },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      gradientToColors: ['#79c280'], // gradient colors
      shadeIntensity: 1,
      type: 'horizontal',
      opacityFrom: 0.7,
      opacityTo: 0.8,
      stops: [0, 100]
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: '#919090' // Set the y-axis label color to white
      },
      formatter: function (value) {
        return `${currency} ${value.toLocaleString()}`;
      }
    }
  },
  tooltip: {
    y: {
      formatter: function (value) {
        return `${currency} ${value.toLocaleString()}`;
      }
    },
    marker: {
      show: true
    }
  },
  legend: {
    position: 'bottom',
    labels: {
      colors: '#919090' // Set the legend label color to white
    }
  },
  grid: {
    show: true,
    borderColor: '',
    strokeDashArray: 0,
    position: 'back',
    xaxis: {
      lines: {
        show: true
      }
    },
    yaxis: {
      lines: {
        show: true
      }
    },
  }
};

var chart = new ApexCharts(document.querySelector("#profitStatusChart"), options);
chart.render();

