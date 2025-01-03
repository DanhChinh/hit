



var gameinfo_list = [];
var gameinfo = undefined;

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

                gameinfo_list.push(JSON.parse(JSON.stringify(GAME_INFO)))



                HISTORY_PROFITS.game.push(GAME_INFO.gameprofit)
                // let playerprofit = 0;
                // HISTORY_PROFITS.player.push(playerprofit)

                CHART.game = drawChart(HISTORY_PROFITS.game, "DOM_gameChart", CHART.game);
                // CHART.player = drawChart(HISTORY_PROFITS.player, "DOM_myChart", CHART.player);

            } else if (received_data["d"] && received_data['d']['bs']) {
                // GAME_INFO.update(received_data);
                // GAME_INFO.show();
                COUNTER.timer +=1;
                console.log(COUNTER.timer)
                if(COUNTER.timer == 10 ){
                    console.log("socket_io.send()")
                    socket_io.send(JSON.stringify(
                        gameinfo_list
                    ))
                };

            }
            else {

            }
        }
        else {
            if (received_data === true) {
                socket.send(JSON.stringify(MESSAGE_WS.info));
                console.log("send MESSAGE_WS.info")
                setTimeout(() => {

                    //fix COUNTER.send = 1;
                    sendInterval = setInterval(() => {
                        socket.send(JSON.stringify(MESSAGE_WS.result(COUNTER.send)));
                        // console.log(JSON.stringify(MESSAGE_WS.result(COUNTER.send)))
                        COUNTER.send++;
                    }, 5000)
                }, 5000)

            }
        }


    };

    socket.onclose = function (event) {
        clearInterval(sendInterval);
        console.log('Kết nối WebSocket đã đóng.');
        alert('Kết nối WebSocket đã đóng.');

    };

    socket.onerror = function (error) {
        console.error('Lỗi WebSocket:', error);
    };
    return socket;

}




var GAME_INFO = {
    profitList: [],
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
            this.prf = this[`mB`] - this[`mW`];
            if (this.rs18 < 11) {
                this.prf *= -1
            }
            this.profitList.push(this.prf);
            
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
        console.log(`Timer: ${this.timer}`)
        console.log(this.profitList)
        console.log(`${formatn(this.moneyOfBlack)} (${this.usersOfBlack}) | ${formatn(this.moneyOfWhite)} (${this.usersOfWhite})`)
        if (this.xx1) {
            console.log(this.xx1, this.xx2, this.xx3);
            console.log("gameprofit:", formatn(this.gameprofit));
        }
        console.groupEnd()
    }
}
function make_game_state() {
    //state: 
    let state = "";

    return state;
}

