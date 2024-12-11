
function mapValue(value, oldMin=0, oldMax=REMOTE.gameMax, newMin=0, newMax=REMOTE.myMax) {
    console.log(value, oldMax, newMax)
    let newValue =  newMin + ((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin);
    return Math.min(newValue, newMax)
}
function normalization(value){
    return Math.round(value / 1000) * 1000;
}
var formatn = number => numeral(number).format('0,0');


function sendMessage(b, sid, eid,){
    console.log(b, sid, eid)
    let message = JSON.stringify(MESSAGE_WS.bet(b, sid, eid));
    if (!b || !sid || !eid || !REMOTE.isPlay) {return 0; }
    socket.send(message);

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
    'predict':undefined,
    'bet':0,
    'make_predict': function(moneyOfBig, moneyOfSmall){
        this['bet'] = Math.abs(moneyOfBig - moneyOfSmall)
        moneyOfBig < moneyOfSmall ? this['predict']='big' : this['predict']='small';

        console.log(this['predict'], formatn(this['bet']))
    },
    'update': function(result){
        let convertresult = result>10? 'big' : 'small';
        console.log(this['predict'], convertresult)
        let reward =  convertresult == this['predict'] ? this['bet'] : -this['bet'];
        this['bet'] = 0
        this['predict'] = undefined;
        return reward;

    }
}

