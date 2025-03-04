

function makeCharts(dom_id) {
    return {
        echarts: echarts.init(document.getElementById(dom_id)),
        data_bar: [],
        data_line: [],
        data_total: 0,
        data_index:[],
        text: dom_id,
        drawEcharts: function () {



            let option = {
                title: {
                    text: this.text,
                    subtext: 'Bar: Giá trị, Line: Cộng dồn'
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
                        smooth: true  // Làm mượt đường line
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

        // Tính toán lại giá trị cộng dồn

        // Cập nhật lại dữ liệu cho biểu đồ
    }
}

var chart_market = makeCharts('chart_market')
var chart_bot = makeCharts('chart_bot')
var chart_investors = makeCharts('chart_investors')
chart_market.drawEcharts()
chart_bot.drawEcharts()
chart_investors.drawEcharts()
