var myChart = echarts.init(document.getElementById('bigmap'));

// Dữ liệu ban đầu
var data = [5, 20, 36, 10, 10];

// Cấu hình đồ thị
var option = {
    title: {
        text: 'Biểu đồ cột động'
    },
    tooltip: {},
    xAxis: {
        data: ['A', 'B', 'C', 'D', 'E']
    },
    yAxis: {},
    series: [{
        name: 'Số lượng',
        type: 'bar',
        data: data
    }]
};
myChart.setOption(option);

