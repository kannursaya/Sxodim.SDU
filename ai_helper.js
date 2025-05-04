// Store the history of messages
let chatHistory = [{"role": "system", "content": "You are a helpful AI assistant to university students."}];

// Function to append new message to the chat box
function appendMessage(role, content) {
    const chatBox = document.getElementById("chat-box");
    const message = document.createElement("p");
    message.classList.add(role);
    message.textContent = content;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest message
}

// Handle sending a message
document.getElementById("send-btn").addEventListener("click", function() {
    const userInput = document.getElementById("user-input").value.trim();
    if (userInput) {
        // Add user input to chat history and display in the chat box
        chatHistory.push({role: "user", content: userInput});
        appendMessage("user", "You: " + userInput);
        
        // Clear input field
        document.getElementById("user-input").value = "";

        // Call the backend API to get the AI's response
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput, history: chatHistory })
        })
        .then(response => response.json())
        .then(data => {
            // Display AI response in the chat box
            const aiMessage = data.reply;
            chatHistory.push({role: "assistant", content: aiMessage});
            appendMessage("assistant", "AI: " + aiMessage);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
