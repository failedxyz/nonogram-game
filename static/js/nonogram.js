const REQUEST_INFO_INTERVAL = 5000;
var socket = io.connect("/"), connection_key, last_update_time = Date.now(), requested = false;
var channels = [];

var encrypt = function (data) {
    var iv = CryptoJS.lib.WordArray.random(16);
    var encrypted = CryptoJS.AES.encrypt(data, CryptoJS.enc.Utf8.parse(connection_key), {
        iv: iv
    });
    return iv.concat(encrypted.ciphertext).toString(CryptoJS.enc.Base64);
};

var decrypt = function (ciphertext) {
    ciphertext = CryptoJS.enc.Base64.parse(ciphertext);
    var iv = ciphertext.clone();
    iv.sigBytes = 16;
    iv.clamp();
    ciphertext.words.splice(0, 4);
    ciphertext.sigBytes -= 16;
    var decrypted = CryptoJS.AES.decrypt({ciphertext: ciphertext}, CryptoJS.enc.Utf8.parse(connection_key), {
        iv: iv
    });
    var data = decrypted.toString(CryptoJS.enc.Utf8);
    return data;
};

var update_loop = function () {
    if (connection_key) {
        if (!requested && Date.now() - last_update_time > REQUEST_INFO_INTERVAL) {
            socket.emit("data", "002" + encrypt("hei"));
            requested = true;
        }
    }
    requestAnimationFrame(update_loop);
};

socket.on("connect", function () {
    socket.emit("data", "001");
    socket.on("data", function (data) {
        var header = parseInt(data.substring(0, 3));
        var raw_body = data.substring(3);
        if (header > 1)
            raw_body = decrypt(raw_body);
        var body = JSON.parse(raw_body);
        switch (header) {
            case 1:
                connection_key = body["key"];
                update_loop();
                break;
            case 2:
                channels = body;
                last_update_time = Date.now();
                requested = false;
                break;
        }
    });
});