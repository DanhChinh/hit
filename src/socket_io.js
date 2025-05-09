



function connectToSocketServer() {
    const serverUrl = "http://localhost:5000";
    try {
        socket_io = io(serverUrl, {
            timeout: 5000, 
            reconnection: true 
        });

        socket_io.on("connect", () => {
            console.log("Kết nối thành công tới pyserver", serverUrl);
            setInterval(()=>{
                let mgs = {
                    "time":new Date(),
                    "data": Math.random()
                }
                socket_io.send(mgs)
                console.log("send:", mgs)
            }, 15000)

        });
        socket_io.on('response',  mgs=> {
            console.log("receive", mgs)
                });
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

