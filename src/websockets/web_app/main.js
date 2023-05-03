socketManager = function() {
  // Private variables and methods
  const chunk_size = 1000; // in milliseconds

  let webSocket = undefined;
  let mediaRecorder = undefined;
  /*let sleep = function (ms) {
    // a function that waits for a given amount of time in milliseconds
    return new Promise(resolve => setTimeout(resolve, ms));
  }*/

  // Public variables and methods
  return {
    start: function() {
      console.log('start');
      let serverIP = document.getElementById('ip').value;
      let serverPort = document.getElementById('port').value;
      let url = 'ws://' + serverIP + ':' + serverPort;
      webSocket = new WebSocket(url);
      webSocket.binaryType = 'blob';
      webSocket.onopen = event => {
        console.log('info: connected to server');

        navigator.mediaDevices
          .getUserMedia({ audio: true, video: false })
          .then(stream => {
            mediaRecorder = new MediaRecorder(stream, {
              mimeType: 'audio/webm',
            });
          
            mediaRecorder.addEventListener('dataavailable', event => {
              if (event.data.size > 0) {
                webSocket.send(event.data);
              }
            });

            mediaRecorder.addEventListener('stop', event => {
              webSocket.close();
            })
            
            mediaRecorder.start(chunk_size);
        });
      };

      webSocket.onmessage = event => {
        console.log(event.data);
      };
    },

    stop: function() {
      console.log('info: disconnected from server');
      mediaRecorder.stop();
      // webSocket.close();
    },

    /*toggle: function(connect_button) {
      if (connect_button.value == "off") {  
        connect_button.value = "on";
        connect_button.innerText = 'Disconnect';
        this.start();
      } else {
        connect_button.value = "off";
        connect_button.innerText = 'Connect';
        this.stop();
      }
    }*/
  };
}(); // gross. - T

function toggle(connect_button) {
  if (connect_button.value == "off") {  
    connect_button.value = "on";
    connect_button.innerText = 'Disconnect';
    socketManager.start();
  } else {
    connect_button.value = "off";
    connect_button.innerText = 'Connect';
    socketManager.stop();
  }
}