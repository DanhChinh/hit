function drawChart(dataArray, domId, charVariable) {
    // const dataToPlot = dataArray.length > 100 ? dataArray.slice(-100) : dataArray;
    const dataToPlot = dataArray;

    // Tính toán giá trị cộng dồn
    const cumulativeSum = [];
    dataToPlot.reduce((acc, curr) => {
        const newSum = acc + curr;
        cumulativeSum.push(newSum);
        return newSum;
    }, 0);
    // let backgroundColors = dataToPlot.map(value => value < 0 ? 'rgba(255, 99, 132, 0.2)' : 'rgba(54, 162, 235, 0.2)');

    // Nếu biểu đồ đã được khởi tạo, cập nhật dữ liệu
    if (charVariable) {
        charVariable.data.labels = dataToPlot.map((_, index) => index + 1);
        charVariable.data.datasets[0].data = dataToPlot;
        charVariable.data.datasets[1].data = cumulativeSum;
        charVariable.update(); // Cập nhật biểu đồ
    } else {
        // Thiết lập biểu đồ lần đầu
        const ctx = document.getElementById(domId).getContext('2d');
        charVariable = new Chart(ctx, {
            type: 'bar', // Biểu đồ dạng cột
            data: {
                labels: dataToPlot.map((_, index) => index + 1), // Vị trí các phần tử
                datasets: [{
                    label: 'Giá trị',
                    data: dataToPlot,
                    backgroundColor: "rgba(5, 42, 79, 0.3)",
                    borderColor: 'black',
                    borderWidth: 1,
                }, {
                    label: 'Cộng dồn',
                    data: cumulativeSum,
                    type: 'line', // Đường line cho cộng dồn
                    fill: true,
                    borderColor: 'rgba(0, 244, 0)',
                    tension: 0.1,
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    return charVariable;
}

var CHART = {
    "game": undefined,
    "player": undefined
}