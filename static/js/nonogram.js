const REQUEST_INFO_INTERVAL = 5000;

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

var app = angular.module("nonogram", []);
app.controller("main-controller", ["$scope", function ($scope) {
    var nonogram = this;
    window.nonogram = nonogram;
    nonogram.available_channels = [];
    nonogram.channels = [];
    nonogram.joined = false;
    nonogram.last_update_time = Date.now();
    nonogram.requested = false;
    nonogram.socket = io.connect("/");

    nonogram.send = function (header, message) {
        nonogram.socket.emit("data", header + encrypt(message));
        console.log(">>", parseInt(header) + ":", message);
        $scope.$apply();
    };

    var update_loop = function () {
        if (connection_key) {
            if (!nonogram.joined) {
                if (!nonogram.requested && Date.now() - nonogram.last_update_time > REQUEST_INFO_INTERVAL) {
                    nonogram.send("002", "hei");
                    nonogram.requested = true;
                }
            } else {

            }
        }
        $scope.$apply();
        requestAnimationFrame(update_loop);
    };

    nonogram.socket.on("connect", function () {
        nonogram.socket.emit("data", "001");
        nonogram.socket.on("data", function (data) {
            var header = parseInt(data.substring(0, 3));
            var raw_body = data.substring(3);
            if (header > 1)
                raw_body = decrypt(raw_body);
            var body = JSON.parse(raw_body);
            console.log("<<", header, raw_body);
            switch (header) {
                case 1:
                    connection_key = body["key"];
                    update_loop();
                    break;
                case 2:
                    nonogram.available_channels = body;
                    var to_join = [];
                    for (var i = 0; i < nonogram.available_channels.length; i += 1) {
                        if (nonogram.available_channels[i].autojoin) {
                            to_join.push(nonogram.available_channels[i].name);
                        }
                    }
                    nonogram.send("003", JSON.stringify(to_join));
                    nonogram.last_update_time = Date.now();
                    nonogram.requested = false;
                    break;
                case 3:
                    var currently_active = nonogram.channels.length ? nonogram.channels[0].name : null;
                    for (var i = 0; i < nonogram.channels.length; i += 1) {
                        if (currently_active == null || nonogram.channels[i].active) {
                            currently_active = nonogram.channels[i].name;
                        }
                    }
                    nonogram.channels = body;
                    if (nonogram.channels.length)
                        nonogram.joined = true;
                    if (currently_active != null) {
                        for (var i = 0; i < nonogram.channels.length; i += 1) {
                            if (nonogram.channels[i].name == currently_active) {
                                nonogram.channels[i].active = true;
                            }
                        }
                    } else if (nonogram.channels.length > 0) {
                        nonogram.channels[0].active = true;
                    }
                    break;
            }
            $scope.$apply();
        });
    });
}]);