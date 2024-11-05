document.addEventListener("DOMContentLoaded", function () {
    const chatLog = document.getElementById("chat-log");
    const chatMessageInput = document.getElementById("chat-message-input");
    const chatMessageSend = document.getElementById("chat-message-send");

    // Configuração do WebSocket
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/lobby/'  // Nome da sala "lobby"
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", "message-received");
        messageElement.textContent = data.message;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
    };

    // Envio de mensagem
    chatMessageSend.onclick = function () {
        const message = chatMessageInput.value;
        if (message) {
            // Exibir mensagem enviada no chat
            const messageElement = document.createElement("div");
            messageElement.classList.add("chat-message", "message-sent");
            messageElement.textContent = message;
            chatLog.appendChild(messageElement);
            chatLog.scrollTop = chatLog.scrollHeight;

            // Enviar a mensagem via WebSocket
            chatSocket.send(JSON.stringify({ "message": message }));
            chatMessageInput.value = "";
        }
    };

    chatMessageInput.onkeyup = function (e) {
        if (e.keyCode === 13) {  // Enviar com Enter
            chatMessageSend.click();
        }
    };
});
