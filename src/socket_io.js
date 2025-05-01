



function connectToSocketServer() {
    const serverUrl = "http://localhost:5000";
    try {
        socket_io = io(serverUrl, {
            timeout: 5000, // Thời gian chờ kết nối (ms)
            reconnection: true // Không tự động kết nối lại
        });

        // Xử lý sự kiện 'connect'
        socket_io.on("connect", () => {
            console.log("Kết nối thành công tới pyserver", serverUrl);
            // showNotification("Kết nối thành công tới pyserver")
        });
        socket_io.on('response', function (data) {
                    let received_data = JSON.parse(data);
                    console.log(received_data.predictions)
                    server_predictions = received_data.predictions
                    
                    // standard.eid =  received_data.eid;
                    // standard.b = received_data.b;

                    // PLAYER.eid = received_data.eid
                    // PLAYER.b = received_data.b * document.getElementById('slider').value;
                    // sendMessage(PLAYER.b, GAME_INFO.sid, PLAYER.eid)
            
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


var socket_io;

