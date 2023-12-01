const socket = io({autoConnect: false});

document.getElementById("join-btn").addEventListener("click", function() {
    let username = document.getElementById("username").value;

    socket.connect();

    socket.on("connect", function() {
        socket.emit("user_join", username);
    })

    document.getElementById("chat").style.display = "block";
    document.getElementById("landing").style.display = "none";
})


document.getElementById("send_private_message").addEventListener("click", function (event) {
    let recipient = document.getElementById("send_to_username").value;
    let message = document.getElementById("private_message").value;
    socket.emit('private_message',  recipient, message);
    document.getElementById("private_message").value = "";
})
socket.on('new_private_message', function(msg) {
    alert(msg);
});

socket.on("chat", function(data) {
    let ul = document.getElementById("chat-messages");
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    ul.appendChild(li);
    ul.scrolltop = ul.scrollHeight;
})