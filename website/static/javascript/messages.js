var socketio;
let sessionUserEmail;
let content;
let isSocketInitialized = false;

fetch('/get-email')
    .then(response => response.json())
    .then(data => {
      sessionUserEmail = data.email;
    })
    .catch(error => {
      console.error('Error fetching email:', error);
    });

function initializeSocketIO() {
  if (isSocketInitialized) {
    socketio.disconnect();
  }

  socketio = io();

  const messages = $("#messages");
  const createMessage = (name, msg) => {
    if (sessionUserEmail == name){
      content = `
      <div class="message_box">
          <span>
              ${msg}
          </span>
      </div>
      `;
    }
    else{
      content = `
      <div class="message_box_other">
          <span>
              ${msg}
          </span>
      </div>
      `;
    }
    
    messages.append(content);
  };

  socketio.on("message", (data) => {
    createMessage(data.name, data.message);
  });

  isSocketInitialized = true;
}

function sendMessage() {
  const message = $("#message");
  if (message.val() === "") return;
  socketio.emit("message", { data: message.val() });
  message.val("");
}

$(".chatForm").on("submit", function (event) {
  event.preventDefault();
});

$("#send-btn").on("click", function (event) {
  event.preventDefault();
  sendMessage();
});

$("#message").on("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
