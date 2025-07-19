var isPlay = false;
var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
var isReverse = false;
var accessTokenStorege = localStorage.getItem("accessToken");
DOM_accessToken.value = accessTokenStorege;


DOM_isPlay.onclick = (e) => {
  isPlay = !isPlay;
  e.target.textContent = isPlay ? "Playing..." : "play";
  e.target.style.backgroundColor = isPlay ? "green" : "red";
};


DOM_isConnectGame.onclick = (e) => {
  if (DOM_accessToken.value) {
    accessToken = DOM_accessToken.value;
    localStorage.setItem("accessToken", accessToken);
  } else {
    return;
  }
  isConnectGame = !isConnectGame;
  e.target.textContent = isConnectGame ? "Connected" : "Connect";
  e.target.style.backgroundColor = isConnectGame ? "green" : "red";

  isConnectGame ? socket_connect() : socket.close();
};
const slider = document.getElementById("slider");
const valueDisplay = document.getElementById("valueDisplay");

slider.addEventListener("input", function () {
  valueDisplay.textContent = slider.value;
});
DOM_reverse.onclick = (e) => {
  isReverse = !isReverse;
  e.target.textContent = isReverse ? "Reverse..." : "no Reverse";
  e.target.style.backgroundColor = isReverse ? "black" : "blue";
};
var socket_io = undefined;

DOM_connectPyserver.onclick = (e) => {
  socket_io = io("http://localhost:5000");

  socket_io.on("connect", () => {
    console.log("✅ Đã kết nối tới server!");
    e.target.textContent = "Connected" ;
    e.target.style.backgroundColor = "green" ;
  });
  socket_io.on("server_message", (msg) => {
    console.log("📩 Server: " + JSON.stringify(msg));
    prd = msg.predict
    if(isReverse){
      prd = prd == 1? 2: 1;
    }
    value = msg.value
    sendMessageToGame(slider.value * value, record.sid, prd);
});
socket_io.on("train_map", (results) => {
  console.log("📩 Nhận dữ liệu từ server:", results);
  const chartsContainer = document.getElementById("echart");
  chartsContainer.innerHTML = ""; // clear cũ

  Object.entries(results).forEach(([modelName, data]) => {
    const scatterId = `scatter-${modelName}`;
    const cumsumId = `cumsum-${modelName}`;

    // Tạo 2 khung
    chartsContainer.innerHTML += `
      <div class="chart-box" id="${scatterId}"></div>
      <div class="chart-box" id="${cumsumId}"></div>
    `;

    // ---------------- Scatter ----------------
    const scatterChart = echarts.init(document.getElementById(scatterId));
    const scatterOption = {
      title: { text: `${modelName} - Scatter (Acc: ${data.accuracy}%)` },
      xAxis: { name: "Dim 1" },
      yAxis: { name: "Dim 2" },
      tooltip: {
        formatter: (p) => `Pred: ${p.data[2]}<br>True: ${p.data[3]}`
      },
      series: [{
        symbolSize: 8,
        data: data.scatter.map(p => [p.x, p.y, p.pred, p.true]),
        type: 'scatter',
        encode: { tooltip: [2, 3] },
        itemStyle: {
          color: (params) => {
            return params.data[2] === params.data[3] ? 'green' : 'red';
          }
        }
      }]
    };
    scatterChart.setOption(scatterOption);

    // ---------------- Cumulative ----------------
    const cumsumChart = echarts.init(document.getElementById(cumsumId));
    const cumsumOption = {
      title: { text: `${modelName} - Cộng dồn đúng/sai` },
      xAxis: { type: 'category', name: "Mẫu" },
      yAxis: { type: 'value', name: "Tổng điểm" },
      tooltip: { trigger: 'axis' },
      series: [{
        data: data.cumsum,
        type: 'line',
        smooth: true,
        lineStyle: { color: 'blue' },
        markLine: {
          data: [{ yAxis: 0 }],
          lineStyle: { type: 'dashed', color: 'gray' }
        }
      }]
    };
    cumsumChart.setOption(cumsumOption);
  });
});

};