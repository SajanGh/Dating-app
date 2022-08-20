const logged_in_user =JSON.parse(document.getElementById('logged_in_user').textContent);


function getChatMessages(user_2){
    $.ajax({
        url:"get_messages/",
        type:'GET',
        headers:{
            "X-Requested-With": "XMLHttpRequest",
        },
        data: {
            'user_2':user_2,
        },
        success:(data) =>{
            $('.msg-body ul').children().hide()
            $('.msg-body ul').html(data)
            console.log("Chat fetched.")
        },
        error:(error) => {
            console.log(error)
        }

    })
}

function setUserDetail(){

    var userName = $('.selected .connection--name').text()
    var userImage = $('.selected .connection--image').attr('src')
    
    $('.user--name').text(userName)
    $('.user--image').attr('src',userImage)

}

jQuery(document).ready(function() {

    $(".chat-list a").click(function() {
        $(".chatbox").addClass('showbox');
        return false;
    });

    $(".chat-icon").click(function() {
        $(".chatbox").removeClass('showbox');
    });

    $('.connection:first').addClass('selected')

    var userId=($('.connection:first').attr('data-userId'))
    getChatMessages(userId)
    setUserDetail()
    var nextURL = window.location.origin+'/chat/?u_id='+userId;
    var nextTitle = 'My new page title';
    var nextState = { additionalInformation: 'Updated the URL with JS' };
    window.history.replaceState(nextState, nextTitle, nextURL)
    setUpWebSocket(userId)
});


$('.connection').click(function(){
    $('.selected').removeClass('selected')
    $(this).addClass('selected')
    var userId=($(this).attr('data-userId'))
    
    getChatMessages(userId)
    setUserDetail()

    var nextURL = window.location.origin+'/chat/?u_id='+userId;
    var nextTitle = 'My new page title';
    var nextState = { additionalInformation: 'Updated the URL with JS' };
    window.history.replaceState(nextState, nextTitle, nextURL)
    setUpWebSocket(userId)
})


var chatSocket = null

function closeWebSocket(){
    if (chatSocket != null){
        chatSocket.close()
        console.log("Socket closed")
        chatSocket = null
    }
}

function setUpWebSocket (userId){
    closeWebSocket();
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + userId
        + '/'
    );
    
    chatSocket.onopen = function(e){
        console.log("New socket opened")
    }
   
     chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.sent_to == $('.selected').attr('data-userId')){

            var list  = document.createElement('li')
            var para = document.createElement('p')
            var chat_span = document.createElement('span')
            chat_span.className = 'time'
            chat_span.innerText = data.timestamp
            para.innerText = data.message
            list.appendChild(para)
            list.appendChild(chat_span)
            if (data.sent_by == logged_in_user.email){
                console.log("maile pathako")
                list.className = 'repaly'
            }else{
                list.className = 'sender'
            }
            $('.chat--messages').append(list)

        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };  


    document.querySelector('#chat-message-input').focus();

    document.querySelector('#chat-message-submit').onclick = function(e) {
        e.preventDefault()
        console.log('Send data')
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'sent_by':logged_in_user['email'],
            'sent_to': $('.selected').attr('data-userId')
        }));
        messageInputDom.value = '';
    };

}