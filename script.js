// script.js file
const _config = {
    qrDelay: 0.5 * 1000, // 10 seconds
}
const _data = {
    name: "",
    score: 0,
    olddate: null,
    totalplayers: [],
}
function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {

    // If found you qr code
    function onScanSuccess(decodeText) {
        //alert("You Qr is : " + decodeText);
        const ournumber = parseInt(decodeText);
        const newdate = new Date().getTime();

        if (Number.isInteger(ournumber)) {
            console.log(_data.olddate);
            if (_data.olddate === null) {
                console.log("made it into olddate");
                _data.olddate = newdate;
                
                _data.score += ournumber;
                document.querySelector("#score").innerText = _data.score; 
            } else {
                const difference = newdate - _data.olddate;
                console.log(difference)
                if (difference > _config.qrDelay) {
                    _data.olddate = newdate;
                    
                    _data.score += ournumber;
                    document.querySelector("#score").innerText = _data.score;
                } else {
                    console.log("cry");
                }
            }
            console.log("date", newdate);
        }
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});

function nameSubmit(event) {
    event.preventDefault();
    var data = document.getElementById("name");
    console.log(data.value);
    _data.name = data.value;
    totalplayers.push(_data.name);
    // overallScore[name] = score
    
}


// The missing semi colons to keep lauren happy
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
