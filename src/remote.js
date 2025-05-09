var isPlay = false;
var isConnectGame = false;
var isConnectMyServer = false;
var accessToken = "";
var accessTokenStorege = localStorage.getItem("accessToken");
DOM_accessToken.value = accessTokenStorege;
DOM_isPlay.onclick = (e) => {
    isPlay = !isPlay;
    e.target.textContent = isPlay ? "View" : "Play";
    e.target.style.backgroundColor = isPlay ? "red" : "green";

}

DOM_isConnectGame.onclick = (e) => {

    if(DOM_accessToken.value){
        accessToken = DOM_accessToken.value;
        localStorage.setItem("accessToken", accessToken);
    }else{
        return;
    }
    isConnectGame = !isConnectGame;
    e.target.textContent = isConnectGame ? "Disconnect Game" : "Connect Game";
    e.target.style.backgroundColor = isConnectGame ? "red" : "green";
}
DOM_isConnectMyServer.onclick = (e)=>{
    isConnectMyServer = !isConnectMyServer;
    e.target.textContent = isConnectMyServer ? "Disconnect My Server" : "Connect My Server";
    e.target.style.backgroundColor = isConnectMyServer ? "red" : "green";
    isConnectMyServer ? connectToSocketServer(): socket_io.close();

}
const slider = document.getElementById('slider');
const valueDisplay = document.getElementById('valueDisplay');

slider.addEventListener('input', function () {
    valueDisplay.textContent = slider.value;
});


