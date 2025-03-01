function leftOrRight(GAME_INFO, server_predictions){
    let b1 = 0;
    let b2 = 0;
    let imm = GAME_INFO['mB']> GAME_INFO['mW']
    let iuu = GAME_INFO['uB']> GAME_INFO['uW']
    for(let predict in predictions){
        let im = predict[0]
        let iu = predict[1]
        let p = predict[2]
        if (im == imm & iu == iuu){
            if (p){b1+=1}else{b2+=1}
        }
    }
    let b = Math.abs(b1 - b2);
    let eid = b1>b2? 1 : 2;

                        standard.eid =  eid;
                    standard.b = b;

                    PLAYER.eid = eid
                    PLAYER.b = b * document.getElementById('slider').value;
                    sendMessage(b, GAME_INFO.sid, eid)
}

function socket_connect() {
    socket = new WebSocket(MESSAGE_WS.url);

    socket.onopen = function (event) {
        console.log('Kết nối WebSocket đã mở.');
        socket.send(JSON.stringify(MESSAGE_WS.login(REMOTE.accessToken)));

    };

    socket.onmessage = function (event) {
        let received_data = JSON.parse(event.data)[1];
        if (typeof received_data === 'object') {
            if (received_data["d"] && received_data['d']['rs']) {
                COUNTER.timer = 0

                GAME_INFO.update(received_data);
                GAME_INFO.show();
                GAME_INFO_ARR.push(JSON.parse(JSON.stringify(GAME_INFO)))
                PLAYER.update(GAME_INFO.rs18);
                standard.update(GAME_INFO.rs18);
                
                socket_io.send(JSON.stringify(GAME_INFO));


                HISTORY_PROFITS.game.push(GAME_INFO.prf)
                HISTORY_PROFITS.standard.push(standard.prf)
                HISTORY_PROFITS.player.push(PLAYER.prf)

                CHART.game = drawChart_2(HISTORY_PROFITS.game, "DOM_gameChart", CHART.game);
                CHART.standard = drawChart_1(HISTORY_PROFITS.standard, "DOM_standard", CHART.standard);
                CHART.player = drawChart_1(HISTORY_PROFITS.player, "DOM_myChart", CHART.player);

            } else if (received_data["d"] && received_data['d']['bs']) {
                GAME_INFO.update(received_data);
                // GAME_INFO.show();
                COUNTER.timer +=1;
                console.log("COUNTER.timer ++")
                if (COUNTER.timer == 20 && server_predictions.lenght >0){
                    leftOrRight(GAME_INFO, server_predictions)
                }

            }
            else {

            }
        }
        else {
            if (received_data === true) {
                socket.send(JSON.stringify(MESSAGE_WS.info));
                console.log("send MESSAGE_WS.info")
                showNotification("Kết nối Game thành công!");
                setTimeout(() => {
                    sendInterval = setInterval(() => {
                        socket.send(JSON.stringify(MESSAGE_WS.result(COUNTER.send)));
                        COUNTER.send++;
                    }, 5000)
                }, 5000)

            }
        }


    };

    socket.onclose = function (event) {
        clearInterval(sendInterval);
        // alert('Kết nối WebSocket đã đóng.');
        setTimeout(()=>{        socket_connect()},1000)

    };

    socket.onerror = function (error) {
        console.error('Lỗi WebSocket:', error);
    };
    return socket;

}




var GAME_INFO = {
    update: function (received_data) {

        this[`mB`] = received_data['d']['bs'][1]['v'];
        this[`mW`] = received_data['d']['bs'][0]['v'];
        this[`uB`] = received_data['d']['bs'][1]['bc'];
        this[`uW`] = received_data['d']['bs'][0]['bc'];
        this.sid = received_data['d']['sid'];
        if (received_data["d"] && received_data['d']['rs']) {
            this.xx1 = +received_data['d']['d1'];
            this.xx2 = +received_data['d']['d2'];
            this.xx3 = +received_data['d']['d3'];
            this.rs18 = this.xx1 + this.xx2 + this.xx3;
            this.prf = Math.abs(this[`mB`] - this[`mW`]);
            if ((this.rs18>10 && this.mB > this.mW) || (this.rs18<11 && this.mB < this.mW)){
                this.prf *= -1;
            }

            
        } else {
            this.xx1 = undefined;
            this.xx2 = undefined;
            this.xx3 = undefined;
            this.rs18 = undefined;
            this.prf = undefined;

        }


    },
    show: function () {
        console.group(`${this.sid}`)
        console.log(`${formatn(this.mB)} (${this.uB}) | ${formatn(this.mW)} (${this.uW})`)
        if (this.xx1) {
            console.log(this.xx1, this.xx2, this.xx3);
            console.log("gameprofit:", formatn(this.prf));
        }
        console.groupEnd()
    }
}

var GAME_INFO_ARR = [];