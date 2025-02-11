
function mapValue(value, oldMin=0, oldMax=REMOTE.gameMax, newMin=0, newMax=REMOTE.myMax) {
    console.log(value, oldMax, newMax)
    let newValue =  newMin + ((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin);
    return Math.min(newValue, newMax)
}
function normalization(value){
    return Math.round(value / 1000) * 1000;
}
var formatn = number => numeral(number).format('0,0');

function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

function sendMessage(b, sid, eid){
    let message = JSON.stringify(MESSAGE_WS.bet(b, sid, eid));
    if (!b || !sid || !eid || !REMOTE.isPlay) {return 0; }
    console.log(b, sid, eid)
    socket.send(message);
    PLAYER.isPlay = false;

}

var MESSAGE_WS = {
    url: "wss://mynygwais.hytsocesk.com/websocket",
    login:(accessToken)=> [1, "MiniGame", "", "", { "agentId": "1", "accessToken": accessToken, "reconnect": false }],
    info: [6, "MiniGame", "lobbyPlugin", { "cmd": 10001 }],
    result: counter => ["7", "MiniGame", "1", counter],
    Hkl: [6, "ShakeDisk", "SD_HoangKimLongPlugin", { "cmd": 1950 }],
    bet: (b, sid, eid) => ["6","MiniGame","taixiuKCBPlugin",{"cmd":2002,"b":b,"sid":sid,"aid":1,"eid":eid,"sqe":true,"a":false}]
}


var HISTORY_PROFITS = {
    "game": [],
    "player": []
}

var COUNTER = {
    "send": 1,
    "round": 0,
    "timer": 0,
    "isEnd":false
}

var PROFITS_LIST_2D = []
var PLAYER_LIST_2D =[]

var socket;
var sendInterval;



var PLAYER = {
    'eid':undefined,
    'b':0,
    'prf':0,
    "timeBet":10,
    "isPlay":false,
    update: function(rs18){
        if(this.eid == 1 && rs18>10  || this.eid == 2 && rs18<11){
            this.prf = this.b
        }else{
            this.prf = -this.b
        }
        this.timeBet = randomInteger(1, 2)
    }
}

