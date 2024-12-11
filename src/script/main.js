




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
                let moneyOfBlack = received_data['d']['bs'][1]['v'];
                let moneyOfWhite = received_data['d']['bs'][0]['v'];
                console.warn(formatn(moneyOfBlack),"___",formatn(moneyOfWhite));
                let gameprofit = moneyOfBlack - moneyOfWhite;
                let xx1 = +received_data['d']['d1'];
                let xx2 = +received_data['d']['d2'];
                let xx3 = +received_data['d']['d3'];
                if (xx1 + xx2 + xx3 > 10) {
                    gameprofit = moneyOfWhite - moneyOfBlack;
                    console.log("result:",1)

                }else{
                    console.log("result:",0)
                }
                let playerprofit = PLAYER.update(xx1+xx2+xx3);
                console.log("gameprofit:", formatn(gameprofit))
                console.log("playerprofit:", formatn(playerprofit))

                HISTORY_PROFITS.game.push(gameprofit)
                HISTORY_PROFITS.player.push(playerprofit)

                CHART.game = drawChart(HISTORY_PROFITS.game, "DOM_gameChart", CHART.game);
                CHART.player = drawChart(HISTORY_PROFITS.player, "DOM_myChart", CHART.player);
                COUNTER.timer = 1;

            } else if (received_data["d"] && received_data['d']['bs']) {
                let moneyOfBlack = received_data['d']['bs'][1]['v'];
                let moneyOfWhite = received_data['d']['bs'][0]['v'];
                console.log(formatn(moneyOfBlack),"___",formatn(moneyOfWhite));

                COUNTER.timer +=1;
                if (COUNTER.timer == 17) {
                    PLAYER.make_predict(moneyOfBlack, moneyOfWhite)
                    let b = normalization(mapValue(PLAYER['bet']))
                    let sid = received_data['d']['sid'];
                    let eid = 1;
                    if(PLAYER['predict'] == 'small'){
                        eid = 2;
                    }
                    PLAYER['bet'] = b;
                    sendMessage(b, sid, eid);
                    

                    // COUNTER.timer = 0;
                }

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



// socket_connect();
