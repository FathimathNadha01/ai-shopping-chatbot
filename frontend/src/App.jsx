import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Show user message
    setMessages(prev => [...prev, { sender: "user", text: input }]);

    const res = await fetch("https://ai-shopping-chatbot-1.onrender.com/api/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();

    // Show bot reply
    setMessages(prev => [...prev, { sender: "bot", text: data.reply }]);
    setInput("");
  };

  return (
    <div style={{ maxWidth: 500, margin: "50px auto", fontFamily: "Arial" }}>
      <h2>🛒 AI Shopping Chatbot</h2>

      <div style={{ border: "1px solid #ccc", padding: 10, minHeight: 200 }}>
        {messages.map((m, i) => (
          <p key={i}>
            <b>{m.sender === "user" ? "You" : "Bot"}:</b> {m.text}
          </p>
        ))}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Type message..."
        style={{ width: "70%", padding: 8 }}
      />
      <button onClick={sendMessage} style={{ padding: 8 }}>
        Send
      </button>
    </div>
  );
}

export default App;
