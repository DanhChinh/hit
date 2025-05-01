function get_time() {
    let currentDate = new Date();

    // Lấy giờ và phút
    let hours = currentDate.getHours().toString().padStart(2, '0');  // Đảm bảo giờ có 2 chữ số
    let minutes = currentDate.getMinutes().toString().padStart(2, '0');  // Đảm bảo phút có 2 chữ số

    // Định dạng theo "giờ:phút"
    let formattedTime = hours + ':' + minutes;
    return formattedTime;
}



var chart_market = {
    echarts: echarts.init(document.getElementById('chart_market')),
    data_bar: [],
    data_line: [],
    data_total: 10_000_000_000,
    data_index: [],
    text: "Market",
    drawEcharts: function () {



        let option = {
            title: {
                text: this.text,
                subtext: 'Market realtime'
            },
            tooltip: {
                trigger: 'axis'
            },
            grid: {
                left: '20%', // Điều chỉnh không gian bên trái để tạo thêm khoảng trống cho trục Y
                top: '20%'
            },
            xAxis: {
                type: 'category',
                data: this.data_index

            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    // fontSize: 14, // Kích thước font cho các nhãn trục Y
                    padding: [0, 10, 0, 10], // Tăng khoảng cách giữa trục Y và các nhãn
                    formatter: function (value) {
                        return `${value / 1_000_000}`
                    } // Đảm bảo định dạng đúng cho giá trị
                }
            },

            series: [
                {
                    name: 'Line',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu cộng dồn cho biểu đồ Line
                    color: '#5470c6',
                    smooth: true,  // Làm mượt đường line,
                    showSymbol: false
                }
            ]
        };

        // Hiển thị biểu đồ ban đầu
        this.echarts.setOption(option);

        // Hàm cập nhật dữ liệu (cập nhật mảng và vẽ lại biểu đồ)
    },
    addItem: function (item) {
        // this.data_bar.push(item);
        this.data_total += item
        this.data_line.push(this.data_total);
        this.data_index.push(get_time());

        this.echarts.setOption({
            xAxis: {
                type: 'category',
                data: this.data_index
            },
            series: [
                {
                    name: 'Line',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu mới cho Line
                }
            ]
        });
    }
}
var chart_bot = {
    echarts: echarts.init(document.getElementById('chart_bot')),
    data_bar: [],
    data_line: [],
    data_total: 0,
    data_index: [],
    text: "Standard",
    drawEcharts: function () {



        let option = {
            title: {
                text: this.text,
                subtext: 'Standard Agl'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Bar', 'Line']
            },
            xAxis: {
                type: 'category',
                data: this.data_index

            },
            yAxis: {
                type: 'value'
            },

            series: [
                {
                    name: 'Bar',
                    type: 'bar',
                    data: this.data_bar,  // Dữ liệu cho biểu đồ Bar
                    color: '#1f77b4'
                },
                {
                    name: 'Line',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu cộng dồn cho biểu đồ Line
                    color: '#ff7f0e',
                    smooth: true,  // Làm mượt đường line
                    showSymbol: false
                }
            ]
        };

        // Hiển thị biểu đồ ban đầu
        this.echarts.setOption(option);

        // Hàm cập nhật dữ liệu (cập nhật mảng và vẽ lại biểu đồ)
    },
    addItem: function (item) {
        this.data_bar.push(item);
        this.data_total += item
        this.data_line.push(this.data_total);
        this.data_index.push(this.data_index.length);

        this.echarts.setOption({
            xAxis: {
                type: 'category',
                data: this.data_index
            },
            series: [
                {
                    name: 'Bar',
                    type: 'bar',
                    data: this.data_bar,  // Dữ liệu mới cho Bar
                },
                {
                    name: 'Line',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu mới cho Line
                }
            ]
        });
    }
}
var chart_investors = {
    echarts: echarts.init(document.getElementById("chart_investors")),
    data_bar: [],
    data_line: [],
    data_total: 1_000_000,
    data_index: [],
    data_total_real: 1_000_000,
    data_line_real: [],
    text: "Investors",
    drawEcharts: function () {



        let option = {
            title: {
                text: this.text,
                subtext: 'Bar: trade, Line: profit'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Bar', 'Line100', 'Line975']
            },
            xAxis: {
                type: 'category',
                data: this.data_index
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: 'Bar',
                    type: 'bar',
                    data: this.data_bar,  // Dữ liệu cho biểu đồ Bar
                    color: '#1f77b4'
                },
                {
                    name: 'Line100',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu cộng dồn cho biểu đồ Line
                    color: '#4AFE07',
                    smooth: true,
                    showSymbol: false
                },
                {
                    name: 'Line975',
                    type: 'line',
                    data: this.data_line_real,  // Dữ liệu cộng dồn cho biểu đồ Line
                    color: '#9309FE',
                    smooth: true,
                    showSymbol: false
                }
            ]
        };

        // Hiển thị biểu đồ ban đầu
        this.echarts.setOption(option);

        // Hàm cập nhật dữ liệu (cập nhật mảng và vẽ lại biểu đồ)
    },
    addItem: function (item) {
        this.data_bar.push(item);
        this.data_total += item
        this.data_line.push(this.data_total);
        this.data_index.push(this.data_index.length);
        this.data_total_real += (item < 0 ? item : 0.975 * item);
        this.data_line_real.push(this.data_total_real);

        this.echarts.setOption({
            xAxis: {
                type: 'category',
                data: this.data_index
            },
            series: [
                {
                    name: 'Bar',
                    type: 'bar',
                    data: this.data_bar,  // Dữ liệu mới cho Bar
                },
                {
                    name: 'Line100',
                    type: 'line',
                    data: this.data_line,  // Dữ liệu mới cho Line
                },
                {
                    name: 'Line975',
                    type: 'line',
                    data: this.data_line_real,  // Dữ liệu mới cho Line
                },
            ]
        });
    }
}




var pie_money = {
    myChart: echarts.init(document.getElementById('pie_money')),
    option: {
        title: {
            text: 'Referer of a Website',
            subtext: 'Fake Data',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: 1048, name: 'Search Engine' },
                    { value: 735, name: 'Direct' },
                    { value: 580, name: 'Email' },
                    { value: 484, name: 'Union Ads' },
                    { value: 300, name: 'Video Ads' }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    },
    drawEcharts: function () {
        this.myChart.setOption(this.option);
    }
}
var pie_user = {
    myChart: echarts.init(document.getElementById('pie_user')),
    option: {
        title: {
            text: 'Referer of a Website',
            subtext: 'Fake Data',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'right'
        },
        series: [
            {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: [
                    { value: 1048, name: 'Search Engine' },
                    { value: 735, name: 'Direct' },
                    { value: 580, name: 'Email' },
                    { value: 484, name: 'Union Ads' },
                    { value: 300, name: 'Video Ads' }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    },
    drawEcharts: function () {
        this.myChart.setOption(this.option);
    }
}


chart_market.drawEcharts()
chart_bot.drawEcharts()
chart_investors.drawEcharts()
pie_money.drawEcharts()
pie_user.drawEcharts()


function makeColor() {
    let chartDom = document.getElementById('Stroke_Animation');
    let myChart = echarts.init(chartDom);
    let option;

    option = {
        graphic: {
            elements: [
                {
                    type: 'text',
                    left: 'center',
                    top: 'center',
                    style: {
                        text: 'Apache ECharts',
                        fontSize: 40,
                        fontWeight: 'bold',
                        lineDash: [0, 200],
                        lineDashOffset: 0,
                        fill: 'transparent',
                        stroke: '#000',
                        lineWidth: 1
                    },
                    keyframeAnimation: {
                        duration: 10000,
                        loop: true,
                        keyframes: [
                            {
                                percent: 0.7,
                                style: {
                                    fill: 'transparent',
                                    lineDashOffset: 200,
                                    lineDash: [200, 0]
                                }
                            },
                            {
                                // Stop for a while.
                                percent: 0.8,
                                style: {
                                    fill: 'transparent'
                                }
                            },
                            {
                                percent: 1,
                                style: {
                                    fill: 'black'
                                }
                            }
                        ]
                    }
                }
            ]
        }
    };

    option && myChart.setOption(option);

}
makeColor()