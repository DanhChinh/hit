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
    data_total: 0,
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
            data_total: 0,
            data_index:[],
            data_total_real: 0,
            data_line_real:[],
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
                            smooth: true,
                            showSymbol: false
                        },
                        {
                            name: 'Line',
                            type: 'line',
                            data: this.data_line_real,  // Dữ liệu cộng dồn cho biểu đồ Line
                            color: '#ff7f0e',
                            smooth: true,
                            showSymbol: false
                        }
                    ]
                };
    
                // Hiển thị biểu đồ ban đầu
                this.echarts.setOption(option);
    
                // Hàm cập nhật dữ liệu (cập nhật mảng và vẽ lại biểu đồ)
            },
            addItem: function(item) {
                this.data_bar.push(item);
                this.data_total += item
                this.data_line.push(this.data_total);
                this.data_index.push(this.data_index.length);
                this.data_total_real += (item<0? item: 0.975*item);
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
                            name: 'Line',
                            type: 'line',
                            data: this.data_line,  // Dữ liệu mới cho Line
                        }
                    ]
                });
            }
        }
chart_market.drawEcharts()
chart_market.addItem(10_000_000_000)
chart_bot.drawEcharts()
chart_investors.drawEcharts()
chart_investors.addItem(1_000_000)

