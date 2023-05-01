/*function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function start() {
    serverIP = document.getElementById('ip').value;
    serverPort = document.getElementById('port').value;
    let url = 'ws://' + serverIP + ':' + serverPort;
    alert(url);
    const webSocket = new WebSocket(url, protocols);
    webSocket.onopen = () => {
        alert("[open] Connection established");
        webSocket.send("Here's some text that the server is urgently awaiting!");
    };
    webSocket.onmessage = (event) => {
        console.log(event.data);
        webSocket.close();
    }
}*/

const webSocket = new WebSocket('ws://localhost:8765');
webSocket.onopen = () => {
    alert("[open] Connection established");
    webSocket.send("Here's some text that the server is urgently awaiting!");
};
webSocket.onmessage = (event) => {
    console.log(event.data);
    webSocket.close();
}