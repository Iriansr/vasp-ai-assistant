// Configure marked.js options
marked.setOptions({
    highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    },
    breaks: true,
    gfm: true
});

const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

// Auto-resize textarea
userInput.addEventListener("input", function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // 👤 Append user message
    appendMessage(text, "user");

    // Clear and reset textarea
    userInput.value = "";
    userInput.style.height = 'auto';

    // 🤖 Append bot loading message
    const botMsgDiv = appendMessage("Thinking...", "bot");
    botMsgDiv.classList.add("loading");

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: text })
        });

        if (!response.ok) throw new Error("Server error");
        
        const data = await response.json();

        // Update bot message with actual answer
        botMsgDiv.classList.remove("loading");
        updateMessageContent(botMsgDiv, data.answer);

        // If there are sources, we could display them too
        if (data.sources && data.sources.length > 0) {
            const sourcesList = data.sources.map(s => `<li><a href="${s.url}" target="_blank">${s.title || s.url}</a></li>`).join("");
            const sourcesHtml = `<div class="sources"><p>Sources:</p><ul>${sourcesList}</ul></div>`;
            botMsgDiv.innerHTML += sourcesHtml;
        }

    } catch (err) {
        console.error(err);
        botMsgDiv.innerText = "Error: Could not connect to the VASP Assistant server. Make sure the backend is running.";
        botMsgDiv.classList.add("error");
    }
}

// Handle Enter key
userInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

function appendMessage(text, type) {
    const msg = document.createElement("div");
    msg.classList.add("message", type);
    
    if (type === "user") {
        msg.innerText = text;
    } else {
        updateMessageContent(msg, text);
    }

    chatBox.appendChild(msg);
    scrollToBottom();

    return msg;
}

function updateMessageContent(element, markdownText) {
    // Parse Markdown
    element.innerHTML = marked.parse(markdownText);
    
    // Render LaTeX
    renderMathInElement(element, {
        delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
        ],
        throwOnError: false
    });

    // Apply code highlighting to new blocks
    element.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    scrollToBottom();
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}
