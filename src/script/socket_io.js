// function socket_io_connect() {
//     socket_io = io('http://localhost:5000');

//     socket_io.on('response', function (data) {
//         let received_data = JSON.parse(data);
//         console.log(received_data)
//         // PLAYER.choice = received_data.content
//         // let index = PLAYER.choice;
//         // if(index %2 == 0){
//         //     PLAYER.value = Math.abs(profit_s40[2])
//         // }else{
//         //     PLAYER.value = Math.floor(Math.abs(profit_s40[1])+Math.abs(profit_s40[3])/2)
//         // }
//         // console.log(PLAYER.choice, PLAYER.value)

//         // send_bet(PLAYER);

//     });

//     socket_io.on('connect', function () {
//         console.log('Đã kết nối tới máy chủ Python');
//     });

//     socket_io.on('disconnect', function () {
//         console.log('Disconnected from server');
//     });
// }
// socket_io_connect();




function connectToSocketServer() {
    const serverUrl = "http://localhost:5000";
    try {
        socket_io = io(serverUrl, {
            timeout: 5000, // Thời gian chờ kết nối (ms)
            reconnection: true // Không tự động kết nối lại
        });

        // Xử lý sự kiện 'connect'
        socket_io.on("connect", () => {
            console.log("Kết nối thành công tới server:", serverUrl);
        });
        socket_io.on('response', function (data) {
                    let received_data = JSON.parse(data);
                    console.log(received_data)
                    PLAYER.eid = received_data.eid
                    PLAYER.b = received_data.b * REMOTE.coefficient
            
                });

        // Xử lý sự kiện 'connect_error'
        socket_io.on("connect_error", (err) => {
            console.error("Lỗi kết nối tới server:", err.message);
        });

        // return socket_io; // Trả về đối tượng socket nếu kết nối thành công
    } catch (error) {
        console.error("Không thể kết nối tới server:", error.message);
        return null; // Trả về null nếu có lỗi
    }
}

// Sử dụng

var socket_io;
// connectToSocketServer();

