// function normalization(gameValue, gameMax, myMax) {
//     let myValue = myMax * gameValue / gameMax;
//     return Math.round(myValue / 500) * 500;
// }
function mapValue(value, oldMin=0, oldMax=1_000_000_000, newMin=0, newMax=100_000) {

    let newValue =  newMin + ((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin);
    return Math.min(newValue, newMax)
}
function normalization(value){

    
    return Math.round(value / 1000) * 1000;
}
var formatn = number => numeral(number).format('0,0');
function Message(header, content, tmp) {
    let counter = 0;
    return { counter, header, content, tmp }
}
function makeChoie(profits) {
    let p1 = profits[1];
    let p2 = profits[2];
    let p3 = profits[3];
    // let sortArr = [p1, p2, p3].sort((a,b)=>a-b);
    let value = Math.max(p1, p2, p3);
    let choice = undefined;
    for (let i = 1; i <= 3; i++) {
        if (profits[i] == value) {
            choice = i;
        }
    }
    return {
        "choice": choice,
        "value": value
    }


}

var calcAvgList = function (list) {
    let list_d3 = list.slice(-3);
    let objAvg = { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5 };
    list_d3.forEach(obj => {
        for (let key in objAvg) {
            objAvg[key] += obj[key] / 3;
        }
    })
    for (let key in objAvg) {
        objAvg[key] = Math.floor(objAvg[key]);
    }
    return objAvg;

}

function objList2Arr(objList) {
    let arr = [];
    objList.forEach(obj => arr = arr.concat(Object.values(obj)))
    return arr;
}

function adjustArray(arr) {
    if (arr.length > 10) {
        // Trả về 10 phần tử cuối của mảng nếu kích thước mảng lớn hơn 10
        return arr.slice(-10);
    } else {
        // Thêm 0 vào đầu mảng cho đến khi mảng có đủ 10 phần tử
        while (arr.length < 10) {
            arr.unshift(0);
        }
        return arr;
    }
}


function make_content(PROFITS_LIST_2D, PLAYER_LIST_2D, history52) {
    if (PROFITS_LIST_2D.length != 39){
        console.log("not fullsize")
        return null;
    }
    let now = new Date();
    let hours = now.getHours();
    let time_frame = (+hours/6)|0;
    let playerDict = {}
    let PLAYER_LIST = PLAYER_LIST_2D.flat();
    PLAYER_LIST.forEach(player=>{
        let dn = player.dn;
        let m = +player.m;
        let eid = +player.b[0].eid;
        let v = +player.b[0].v;
        if(dn in playerDict){
            playerDict[dn][eid]+=v;
            playerDict[dn]["m"] = m;
            
        }else{
            playerDict[dn] = {
                "m": m,
                0:0,
                1:0,
                2:0,
                3:0,
                4:0,
                5:0
            }
            playerDict[dn][eid] = v;

        }
    })
    let arrSort = [];
    for (let key in  playerDict){
        let obj = playerDict[key];
        obj.dn = key;
        arrSort.push(obj)
    }
    arrSort = arrSort.sort((a, b) => a.m - b.m);
    // console.log("playerDict",playerDict);
    // console.log("arrSort",arrSort);

    let profitS =  PROFITS_LIST_2D.flat();
    let userS = arrSort;
    let id = now.toUTCString();
    let parentId = "";
    return {id, parentId, time_frame, hours, profitS, userS, history52}


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
var PLAYER = {
    "choice": undefined,
    "value": 0
}

var PROFITS_LIST_2D = []
var PLAYER_LIST_2D =[]
var GAME_HISTORY52 = []
var messageIO_content = undefined
var profit_s40 = []

var socket;
var socket_io;
var sendInterval;
var old_message;



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