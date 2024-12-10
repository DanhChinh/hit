function socket_io_connect() {
    socket_io = io('http://localhost:5000');

    socket_io.on('response', function (data) {
        let received_data = JSON.parse(data);
        PLAYER.choice = received_data.content
        let index = PLAYER.choice;
        if(index %2 == 0){
            PLAYER.value = Math.abs(profit_s40[2])
        }else{
            PLAYER.value = Math.floor(Math.abs(profit_s40[1])+Math.abs(profit_s40[3])/2)
        }
        console.log(PLAYER.choice, PLAYER.value)

        send_bet(PLAYER);

    });

    socket_io.on('connect', function () {
        console.log('Đã kết nối tới máy chủ Python');
    });

    socket_io.on('disconnect', function () {
        console.log('Disconnected from server');
    });
}
socket_io_connect();