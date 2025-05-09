function sendMessageToGame(b, sid, eid) {
  let message = JSON.stringify(MESSAGE_WS.bet(b, sid, eid));
  console.log("send game:", message);
  if (!b || !sid || !eid || !isPlay) {
    return 0;
  }
  socket.send(message);
}
var MESSAGE_WS = {
  url: "wss://mynylifes.hytsocesk.com/websocket_live",
  login: (accessToken) => [
    1,
    "MiniGame2",
    "",
    "",
    { agentId: "1", accessToken: accessToken, reconnect: false },
  ],
  info: ["6", "MiniGame2", "taixiu_live_gateway_plugin", { cmd: 15000 }],
  result: (counter) => ["7", "MiniGame2", "1", counter],
  Hkl: [6, "ShakeDisk", "SD_HoangKimLongPlugin", { cmd: 1950 }],
  bet: (b, sid, eid) => [
    "6",
    "MiniGame2",
    "taixiu_live_gateway_plugin",
    { cmd: 15002, b: b, sid: sid, aid: 1, eid: eid },
  ],
};

function sendDataToThuhuyenFun(record) {
  if (record.progress.length === 0) {
    return;
  }
  let data = new FormData();
  data.append("sid", record.sid);
  data.append("progress", JSON.stringify(record.progress));
  data.append("d1", record.d1);
  data.append("d2", record.d2);
  data.append("d3", record.d3);
  axios
    .post("https://thuhuyen.fun/xg79/post_data.php", data)
    .then((response) => {
      if (response.data.success) {
        console.log("Dữ liệu đã được lưu trữ thành công");
      } else {
        console.error("Lỗi: " + response.data.message);
      }
    })
    .catch((error) => {
      console.error("Lỗi kết nối:", error);
    });
}
var sendInterval;
var counter_send = 0;
var socket;
var is_betting = false;
var initRecord = (
  sid = undefined,
  progress = [],
  d1 = undefined,
  d2 = undefined,
  d3 = undefined
) => {
  return { sid, progress, d1, d2, d3 };
};
var record = initRecord();

function socket_connect() {
  socket = new WebSocket(MESSAGE_WS.url);

  socket.onopen = function (event) {
    console.log("Kết nối WebSocket đã mở.");
    socket.send(JSON.stringify(MESSAGE_WS.login(accessToken)));
  };

  socket.onmessage = async function (event) {
    let mgs = JSON.parse(event.data)[1];
    if (typeof mgs === "object") {
      //betting
      if (mgs.cmd === 15007 && is_betting) {
        record.progress.push(JSON.parse(JSON.stringify(mgs.bs)));
        console.log(" record.progress.push");
        if (record.progress.length === 40) {
          prd = await predict(JSON.parse(JSON.stringify(record.progress)));
          sendMessageToGame(slider.value, record.sid, prd === 1 ? 1 : 2);
          console.log("prd", prd);
        }
        return;
      }
      //ending
      if (mgs.cmd === 15006) {
        record.sid = mgs.sid;
        record.d1 = mgs.d1;
        record.d2 = mgs.d2;
        record.d3 = mgs.d3;
        sendDataToThuhuyenFun(JSON.parse(JSON.stringify(record)));
        is_betting = false;
        let rs = mgs.d1 + mgs.d1 + mgs.d3;
        console.log("rs18: ", rs);
        rs = rs > 10 ? 1 : 0;
        checkPrd(prd, rs);
        return;
      }
      //start
      if (mgs.cmd === 15005) {
        record = initRecord();
        record.sid = mgs.sid;
        console.log("start", record);
        is_betting = true;
        return;
      }
      //sended
      if (mgs.cmd === 15002) {
        console.log(mgs);
        return;
      }

      if (mgs.cmd === 100) {
        console.log("success: ", mgs);
        return;
      }
    } else {
      if (mgs === true) {
        socket.send(JSON.stringify(MESSAGE_WS.info));
        console.log("send MESSAGE_WS.info");
        setTimeout(() => {
          sendInterval = setInterval(() => {
            socket.send(JSON.stringify(MESSAGE_WS.result(counter_send)));
            counter_send++;
          }, 5000);
        }, 5000);
      }
    }
  };

  socket.onclose = function (event) {
    clearInterval(sendInterval);
    // alert('Kết nối WebSocket đã đóng.');
    setTimeout(() => {
      socket_connect();
    }, 1000);
  };

  socket.onerror = function (error) {
    console.error("Lỗi WebSocket:", error);
  };
  return socket;
}

var is_true = 0;
var is_false = 0;
var prd = undefined;
function checkPrd(prd, rs) {
  if (prd === undefined) {
    return;
  }
  let element = document.createElement("div");
  element.classList.add("round");
  if (prd === rs) {
    is_true += 1;
    element.classList.add("bg_green");
    element.innerText = is_true;
  } else {
    is_false += 1;
    element.classList.add("bg_red");
    element.innerText = is_false;
  }
  DOM_history.appendChild(element);
}
