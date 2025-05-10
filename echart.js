const rawData = [];
        const candleData = [];
        const labels = [];

        const chart = echarts.init(document.getElementById('echart'));

        // Khởi tạo dữ liệu nến ban đầu
        let open = 0;
        for (let i = 0; i < rawData.length; i++) {
            const result = calcCandle(open, rawData[i]);
            candleData.push(result.candle);
            labels.push(`${i + 1}`);
            open = result.close;
        }

        const option = {
            title: { text: 'Biểu đồ Nến Nhật Cập Nhật Trực Tiếp' },
            tooltip: { trigger: 'axis' },
            xAxis: {
                type: 'category',
                data: labels,
                scale: true
            },
            yAxis: { scale: true },
            series: [{
                type: 'candlestick',
                data: candleData,
                itemStyle: {
                    color: '#00b050',       // Nến tăng (Xanh lá)
                    color0: '#ff0000',      // Nến giảm (Đỏ tươi)
                    borderColor: '#00b050',
                    borderColor0: '#ff0000'
                }

            }]
        };

        chart.setOption(option);

        // Hàm tính nến từ giá trị mới
        function calcCandle(open, change) {
            const close = open + change;
            const delta = Math.random() * 2;
            const low = Math.min(open, close) - delta;
            const high = Math.max(open, close) + delta;

            return {
                candle: [
                    open.toFixed(2),
                    close.toFixed(2),
                    low.toFixed(2),
                    high.toFixed(2)
                ],
                close: close
            };
        }

        // Hàm thêm dữ liệu mới và cập nhật biểu đồ
        function addData(newChange) {
            rawData.push(newChange);

            const lastCandle = candleData[candleData.length - 1];
            const lastClose = parseFloat(lastCandle[1]); // lấy close của nến cuối

            const result = calcCandle(lastClose, newChange);
            candleData.push(result.candle);
            labels.push(`Ngày ${labels.length + 1}`);

            chart.setOption({
                xAxis: { data: labels },
                series: [{ data: candleData }]
            });
        }