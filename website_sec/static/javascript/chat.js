$(document).ready(function() {
    const chatBox = $('#chatBox');
    const closeBtn = $('#close-btn');
    const allChatButton = $('#chatStickyBtn');
    const allChat = $('#allChat');
    const allCloseBtn = $('#close-btn-all');
    const backBtn = $('#back-btn');
  
    $(document).on('click', '.chatButton', function() {
      $('#messages').text("");
      chatBox.css('display', 'block');
      allChat.css('display', 'none');
    });
  
    closeBtn.on('click', function() {
      chatBox.css('display', 'none');
    });

    backBtn.on('click', function() {
        $('#conversas').text("");
        chatBox.css('display', 'none');
        allChat.css('display', 'block');
    });
  
    allChatButton.on('click', function() {
      $('#conversas').text("");
      allChat.css('display', 'block');
    });
  
    allCloseBtn.on('click', function() {
      allChat.css('display', 'none');
    });
  
    // Handle the form submission event for chatForm
    $(document).on('submit', '.chatForm', function(event) {
      event.preventDefault(); // Prevent default form submission
      var receiver_value = $(this).find('.chatButton').val(); 
    
      // Send the AJAX request
      $.ajax({
        type: 'POST',
        url: '/team',
        data: {
          'receiver_value':  receiver_value
        },
        success: function(response) {
          var messages = response.messages;
          for (var i = 0; i < messages.length; i++) {
            var message = messages[i];
            if (message.name == response.session_user){
              var html = `
                <div class="message_box">
                  <span>
                    ${message.message} 
                  </span>
                </div>`;
              $('#messages').append(html);
            }
            else {
              var html = `
                <div class="message_box_other">
                  <span>
                    ${message.message} 
                  </span>
                </div>`;
              $('#messages').append(html);
            }
          }
        }
      });
    });
    
  
    // Handle the form submission event for conversationsForm
    $(document).on('submit', '#conversationsForm', function(event) {
      event.preventDefault(); // Prevent default form submission
  
      // Send the AJAX request
      $.ajax({
        type: 'POST',
        url: '/conversations',
        success: function(response) {
          var conversations = response.conversations;
          var names = response.names;
          var types = response.types;
          for (var i = 0; i < conversations.length; i++) {
            var conversation = conversations[i];
            var name = names[i];
            var type = types[i];
            if (type === "0"){
              type = "Admin";
            }
            else {
              type = "Utilizador";
            }
            var html = `
              <form method="post" action="/team" class="chatForm" onsubmit="initializeSocketIO()">
                <button type="submit" class="chatButton" style="width:100%;" value="${conversation}">
                  <span>
                    <strong style="color: rgb(99, 42, 206);">${name}</strong>
                  </span>
                  <span style="color: rgb(99, 42, 206);">${type}</span>
                </button>
                <hr>
              </form>`;
            $('#conversas').append(html);
          }
        }
      });
    });
  });
  