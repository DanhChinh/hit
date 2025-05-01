
function sendMessage(b, sid, eid) {
    console.log(sid, b, eid)
    if (!b || !sid || !eid || !REMOTE.isPlay) { return 0; }
    // showNotification(`${sid}: ${b}->${eid}`)
    let message = JSON.stringify(MESSAGE_WS.bet(b, sid, eid));
    socket.send(message);
    PLAYER.isPlay = false;

}
var MESSAGE_WS = {
    url: "wss://mynylifes.hytsocesk.com/websocket_live",
    login: (accessToken) => [1, "MiniGame2", "", "", { "agentId": "1", "accessToken": accessToken, "reconnect": false }],
    info: ["6", "MiniGame2", "taixiu_live_gateway_plugin", { "cmd": 15000 }],
    result: counter => ["7", "MiniGame2", "1", counter],
    Hkl: [6, "ShakeDisk", "SD_HoangKimLongPlugin", { "cmd": 1950 }],
    bet: (b, sid, eid) => ["6","MiniGame2","taixiu_live_gateway_plugin",{"cmd":15002,"b":b,"sid":sid,"aid":1,"eid":eid}]
}

function randomChoice(arr) {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
}

var counter_send = 0;
var socket;
var is_betting = false;
var record ={
    sid:undefined,
    progress:[],
    d1:undefined,
    d2:undefined,
    d3:undefined,
    reset:function(){
        this.sid = undefined;
        this.progress = [];
        this.d1 = undefined;
        this.d2 = undefined;
        this.d3 = undefined;
    }

};

var predict = randomChoice([1,2])
var result_eid = undefined;
var min_bet = 200;
var bet = min_bet;


function socket_connect() {
    socket = new WebSocket(MESSAGE_WS.url);

    socket.onopen = function (event) {
        console.log('Kết nối WebSocket đã mở.');
        socket.send(JSON.stringify(MESSAGE_WS.login(REMOTE.accessToken)));

    };

    socket.onmessage = function (event) {
        let received_data = JSON.parse(event.data)[1];
        if (typeof received_data === 'object') {
            if (received_data.cmd === 100) {
                console.log("start player infor", received_data)
            } else if (received_data.cmd === 15000) {
                // console.log("start other user infor", received_data)
            }
            else if (received_data.cmd === 15008) {
                // console.log("message", received_data)
            } else if (received_data.cmd === 706) {
                // console.log("user infor", received_data)

            } else if (received_data.cmd === 15007) {
                if(is_betting){
                    // console.log("betting", received_data)
                    record.progress.push(received_data.bs)

                }else{
                    console.log("waiting...")
                }
            } else if (received_data.cmd === 15006) {
                // console.log("result", received_data)
                record.sid = received_data.sid
                record.d1 = received_data.d1;
                record.d2 = received_data.d2;
                record.d3 = received_data.d3;
                console.log(record)
                is_betting = false;

                result_eid =  (received_data.d1 + received_data.d2+received_data.d3)>10? 1: 2;

                if(result_eid === predict){
                    bet = min_bet;
                }else{
                    bet *=2;
                }
                predict = randomChoice([1,2])
            }
            else if (received_data.cmd === 15005) {
                // console.log("newGame", received_data)
                record.reset();
                is_betting = true;

                let messobj = MESSAGE_WS.bet(bet, received_data.sid, predict);
                console.log(messobj);
                socket.send(JSON.stringify(messobj))
            }
            else {
                console.log("other", received_data)
            }
        }
        else {
            if (received_data === true) {
                socket.send(JSON.stringify(MESSAGE_WS.info));
                console.log("send MESSAGE_WS.info")
                // showNotification("Kết nối Game thành công!");
                setTimeout(() => {
                    sendInterval = setInterval(() => {
                        socket.send(JSON.stringify(MESSAGE_WS.result(counter_send)));
                        counter_send++;
                    }, 5000)
                }, 5000)

            }
        }


    };

    socket.onclose = function (event) {
        clearInterval(sendInterval);
        // alert('Kết nối WebSocket đã đóng.');
        setTimeout(() => { socket_connect() }, 1000)

    };

    socket.onerror = function (error) {
        console.error('Lỗi WebSocket:', error);
    };
    return socket;

}


