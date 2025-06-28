var isPlay = false;
var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
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
    value = msg.value
    sendMessageToGame(slider.value * value, record.sid, prd);
});
  // socket_io.on("disconnect", () => {
  //   log("❌ Mất kết nối với server");
  // });

};