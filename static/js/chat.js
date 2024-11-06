// Seleciona os elementos do chat
const openChatButton = document.getElementById('open-chat');
const chatWidget = document.getElementById('chat-widget');
const closeChatButton = document.getElementById('close-chat');
const chatMessageInput = document.getElementById('chat-message-input');
const chatLog = document.getElementById('chat-log');
const sendMessageButton = document.getElementById('chat-message-send');
const addUserButton = document.getElementById('add-user');
const recipientContainer = document.getElementById('recipient-container');
const recipientSelect = document.getElementById('recipient-select');
const startConversationButton = document.getElementById('start-conversation');
let selectedRecipientId = null;

// Abre o chat
openChatButton.addEventListener('click', () => {
    chatWidget.style.display = 'block';
});

// Fecha o chat
closeChatButton.addEventListener('click', () => {
    chatWidget.style.display = 'none';
    recipientContainer.style.display = 'none';
});

// Exibe o seletor de destinatários ao clicar em "+"
addUserButton.addEventListener('click', () => {
    recipientContainer.style.display = 'block';
});

// Inicia a conversa com o destinatário selecionado
startConversationButton.addEventListener('click', () => {
    selectedRecipientId = recipientSelect.value;
    if (selectedRecipientId) {
        recipientContainer.style.display = 'none';
        alert("Conversa iniciada com o usuário selecionado!");
    } else {
        alert("Por favor, selecione um destinatário.");
    }
});

// Envia uma mensagem
sendMessageButton.addEventListener('click', sendMessage);
chatMessageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const message = chatMessageInput.value.trim();
    if (message && selectedRecipientId) {
        fetch('/send_message/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recipient_id: selectedRecipientId,
                content: message,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Message sent!') {
                const messageElement = document.createElement('div');
                messageElement.classList.add('chat-message');
                messageElement.textContent = message;
                chatLog.appendChild(messageElement);

                chatMessageInput.value = '';
                chatLog.scrollTop = chatLog.scrollHeight;
            } else {
                alert(data.status || 'Erro ao enviar a mensagem.');
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            alert('Erro ao enviar a mensagem.');
        });
    } else {
        alert("Por favor, selecione um destinatário e digite uma mensagem.");
    }
}

// Função para obter o valor do CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
