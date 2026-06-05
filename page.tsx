"use client";

import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function askQuestion() {
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json();

      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Error connecting to backend.");
    }

    setLoading(false);
  }

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-4xl font-bold">
        Sujal AI Assistant
      </h1>

      <input
        className="border p-3 mt-6 w-full rounded"
        placeholder="Ask about Sujal..."
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
      />

      <button
        className="mt-4 border px-4 py-2 rounded"
        onClick={askQuestion}
      >
        Ask
      </button>

      <div className="mt-8">
        {loading ? "Thinking..." : answer}
      </div>
    </main>
  );
}