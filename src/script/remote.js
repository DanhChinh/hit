var REMOTE = {
    "isPlay": false,
    "isShowInput": false,
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
DOM_isShowInput.onclick = (e) => {

    REMOTE.isShowInput = !REMOTE.isShowInput;
    e.target.textContent = REMOTE.isShowInput ? "Hide" : "Show";
    document.getElementsByClassName('my_form')[0].style.display = REMOTE.isShowInput ? "block" : "none";

}

DOM_connectWs.onclick = ()=> socket.close();