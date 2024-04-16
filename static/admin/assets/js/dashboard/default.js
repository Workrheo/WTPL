// Revenue Chart
var ctx = document.getElementById('revenueVsExpenseChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Revenue', 'Expense'],
        datasets: [{
            data: [totalRevenue, totalExpense],
            backgroundColor: [
                TivoAdminConfig.primary, // Background color for revenue
                'rgba(255, 99, 132, 0.8)' // Background color for expense
            ],
            borderColor: '#dfdfdfbf', // Border color
            borderWidth: 2, // Border width
            hoverBackgroundColor: [
                '#5d65cf', // Hover background color for revenue
                '#bf3758' // Hover background color for expense
            ],
            hoverOffset: 8 // Increase the offset on hover for a unique effect
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        var label = context.label || '';
                        var value = context.raw || 0;
                        return label + ': ' + value.toLocaleString();
                    }
                }
            }
        }
    }
});

// Profit Chart
var ctx = document.getElementById('profitStatusChart').getContext('2d');
var profit = totalRevenue - totalExpense;

var maxProfit = Math.max(totalRevenue, totalExpense);
maxProfit = Math.ceil(maxProfit / 2) * 2;

var chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Revenue', 'Expense'],
    datasets: [
      {
        label: 'Profit',
        data: [totalRevenue, totalExpense],
        backgroundColor: 'rgba(0, 0, 0, 0)', // Transparent background
        borderColor: profit >= 0 ? '#00C853' : '#FF1744', // Green if profit is positive, red if negative
        borderWidth: 2,
        pointBackgroundColor: profit >= 0 ? '#00C853' : '#FF1744', // Point color matching the line color
        pointRadius: 4,
        pointHoverRadius: 5,
        pointHoverBorderWidth: 2,
        fill: false,
        stepped: true, // Use stepped line chart
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          font: {
            size: 12,
            weight: 'bold',
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            var label = context.label || '';
            var value = context.raw || 0;
            return label + ': ' + value.toLocaleString();
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          // Define the maximum value and steps of your Y axis here
          max: maxProfit,
          min: 0,
          stepSize: maxProfit > 2 ? maxProfit / 2 : 1,
        },
      },
    },
  },
});


// Invoice Status Chart
var ctx = document.getElementById('invoiceStatusChart').getContext('2d');

var maxInvoice = Math.max(paidInvoice, unpaidInvoice);
maxInvoice = Math.ceil(maxInvoice / 2) * 2;

var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Invoices'],
        datasets: [{
            label: 'Paid',
            data: [paidInvoice],
            backgroundColor: 'rgba(60, 179, 113, 0.5)', // Medium sea green color for paid
            borderColor: 'rgba(60, 179, 113, 1)', // Solid medium sea green color for border
            borderWidth: 2 // Border width
        },
        {
            label: 'Unpaid',
            data: [unpaidInvoice],
            backgroundColor: 'rgba(255, 127, 80, 0.5)', // Coral color for unpaid
            borderColor: 'rgba(255, 127, 80, 1)', // Solid coral color for border
            borderWidth: 2 // Border width
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    // Define the maximum value and steps of your Y axis here
                    max: maxInvoice,
                    min: 0,
                    stepSize: maxInvoice > 2 ? maxInvoice / 2 : 1
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
                onClick: function(e, legendItem) {
                    var index = legendItem.datasetIndex;
                    var ci = this.chart;
                    var alreadyHidden = (ci.getDatasetMeta(index).hidden === null) ? false : ci.getDatasetMeta(index).hidden;

                    ci.data.datasets.forEach(function(e, i) {
                        var meta = ci.getDatasetMeta(i);

                        if (i !== index) {
                            if (!alreadyHidden) {
                                meta.hidden = meta.hidden === null ? !meta.hidden : null;
                            } else if (meta.hidden === null) {
                                meta.hidden = true;
                            }
                        } else if (i === index) {
                            meta.hidden = null;
                        }
                    });

                    ci.update();
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        var label = context.dataset.label || '';
                        var value = context.parsed.y || 0;
                        return label + ': ' + value.toLocaleString();
                    }
                }
            }
        }
    }
});

// Task Chart
var ctx = document.getElementById('taskStatusChart').getContext('2d');
ctx.canvas.width = 200; // Set the desired width
ctx.canvas.height = 200; // Set the desired height
var chart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['To Do', 'In Progress', 'Done'],
    datasets: [
      {
        data: [toDoCount, inProgressCount, doneCount],
        backgroundColor: [
          '#FF3B30', // Background color for 'To Do'
          '#FFCC00', // Background color for 'In Progress'
          '#007AFF' // Background color for 'Done'
        ],
        borderColor: '#dfdfdfbf', // Border color
        borderWidth: 2, // Border width
        hoverBackgroundColor: [
          '#BF372D', // Hover background color for 'To Do'
          '#FFB900', // Hover background color for 'In Progress'
          '#005AE0' // Hover background color for 'Done'
        ],
        hoverOffset: 8 // Increase the offset on hover for a unique effect
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          font: {
            size: 12,
            weight: 'bold'
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            var label = context.label || '';
            var value = context.raw || 0;
            return label + ': ' + value.toLocaleString();
          }
        }
      }
    }
  }
});



