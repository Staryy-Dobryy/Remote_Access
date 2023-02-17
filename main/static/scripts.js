let socket = new WebSocket("ws://127.0.0.1:8081");
let socket2 = new WebSocket("ws://10.0.2.15:8081");

socket2.onopen = function (event){
    console.log("CONNECTION OPEN")
    socket2.onmessage = function (event) {
        document.getElementById("frame-1").style.backgroundImage = document.getElementById("frame-2").style.backgroundImage
        document.getElementById("frame-2").style.backgroundImage = event.data;
    };
}
document.addEventListener('click', function (event) {
if (!event.target.hasAttribute('data-fullscreen')) return;
document.getElementById("stream-screen").requestFullscreen();
}, false);

addEventListener('fullscreenchange', (event) => {
    if (document.fullscreenElement) {
        document.getElementById("load").style.display = "none";
        socket.send("STREAM|1")
    } 
    else {
        document.getElementById("load").style.display = "block";
        socket.send("0")
    }
});