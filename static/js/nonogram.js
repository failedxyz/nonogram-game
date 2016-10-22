var socket = io.connect("/");

socket.on("connect", function () {
    socket.emit("data", "001");
    socket.on("data", function (data) {
        var header = parseInt(data.substring(0, 3));
        var body = JSON.parse(data.substring(3));
        console.log(header, body);
    });
});