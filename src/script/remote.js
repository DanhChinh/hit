var REMOTE = {
    "isPlay": false,
    "isShowInput": false,
    "isConnect": false,
    "accessToken": undefined,
    "coefficient": 10000

}

DOM_isPlay.onclick = (e) => {
    
    REMOTE.isPlay = !REMOTE.isPlay;
    e.target.textContent = REMOTE.isPlay ? "View" : "Play";
    e.target.style.backgroundColor = REMOTE.isPlay ? "red" : "green";
    if (REMOTE.isPlay) {
        REMOTE.coefficient = slider.value;
    }
}
DOM_isShowInput.onclick = (e) => {

    REMOTE.isShowInput = !REMOTE.isShowInput;
    e.target.textContent = REMOTE.isShowInput ? "Hide" : "Show";
    document.getElementsByClassName('my_form')[0].style.display = REMOTE.isShowInput ? "block" : "none";

}
DOM_isConnect.onclick = (e)=>{
    REMOTE.isConnect =!REMOTE.isConnect;
    REMOTE.accessToken = DOM_accessToken.value;
    e.target.textContent = REMOTE.isConnect? "Disconnect" : "Connect";
    e.target.style.backgroundColor = REMOTE.isConnect? "red" : "green";
    if (REMOTE.isConnect) {
        connectToSocketServer();
        socket_connect();
    } else {
        if (socket) {
            socket.close();
            socket_io.disconnect();
        }
    }
}

const slider = document.getElementById('slider');
        const valueDisplay = document.getElementById('valueDisplay');

        slider.addEventListener('input', function() {
            valueDisplay.textContent = slider.value;
        });