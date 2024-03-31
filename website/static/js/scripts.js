
const purchaseOrdersData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    series: [
        [30, 40, 35, 50, 49],
        // Add more series if needed
    ],
};

const salesOrdersData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    series: [
        [20, 35, 25, 45, 30],
        // Add more series if needed
    ],
};


// Mixed Chart: Purchase Orders and Sales Orders
const mixedChartOptions = {
    chart: {
        height: 350,
        type: 'line',
        stacked: false,
    },
    dataLabels: {
        enabled: false,
    },
    series: [{
        name: 'Auction Orders',
        type: 'area',
        data: purchaseOrdersData.series[0],
    }, {
        name: 'Sales Orders',
        type: 'area',
        data: salesOrdersData.series[0],
    }],
    xaxis: {
        categories: purchaseOrdersData.labels,
    },
};

// Render the charts

const mixedChart = new ApexCharts(document.getElementById('mixedChart'), mixedChartOptions);


mixedChart.render();


// CUSTOMER CHART: Customer Growth Over Time
const customerChartOptions = {
    series: [
      {
        name: 'Customers',
        data: [10, 25, 35, 45, 55, 65, 75], 
      },
    ],
    chart: {
      type: 'line',
      height: 350,
      toolbar: {
        show: false,
      },
    },
    colors: ['#4f35a1'],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth',
    },
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'], 
    },
    yaxis: {
      title: {
        text: 'Number of Dolbel Customers',
      },
    },
  };
  
  const customerChart = new ApexCharts(
    document.querySelector('#customerChart'),
    customerChartOptions
  );
  customerChart.render();