var REMOTE = {
    "isPlay": false,
    "isShowProfits": false,
    "gameMax": undefined,
    "myMax": undefined

}

DOM_isPlay.onclick = (e) => {
    REMOTE.isPlay = !REMOTE.isPlay;
    e.target.textContent = REMOTE.isPlay ? "Stop" : "Start";
    e.target.style.backgroundColor = REMOTE.isPlay ? "red" : "green";
    if (REMOTE.isPlay) {
        REMOTE.gameMax = +DOM_gameMax.value;
        REMOTE.myMax = +DOM_myMax.value;
    }
}
DOM_isShowProfits.onclick = (e) => {
    REMOTE.isShowProfits = !REMOTE.isShowProfits;
    e.target.textContent = REMOTE.isShowProfits ? "HideP" : "ShowP";
    document.getElementsByClassName('DOM_profits')[0].style.display = REMOTE.isShowProfits ? "block" : "none";

}

DOM_connectWs.onclick = ()=> socket.close();
DOM_connectWsIO.onclick = ()=> socket_io.close();