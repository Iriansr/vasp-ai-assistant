async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const text = input.value;
    if (!text) return;

    // 👤 user message
    appendMessage(text, "user");

    input.value = "";

    // 🤖 loading message
    const loading = appendMessage("...", "bot");

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: text })
        });

        const data = await response.json();

        loading.innerText = data.answer;

    } catch (err) {
        loading.innerText = "Error connecting to server.";
    }
}

document.getElementById("user-input").addEventListener("keydown", function (event) {
    
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

function appendMessage(text, type) {

    const chatBox = document.getElementById("chat-box");

    const msg = document.createElement("div");
    msg.classList.add("message", type);
    msg.innerHTML = marked.parse(text);

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;

    return msg;
}