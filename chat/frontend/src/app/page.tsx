'use client';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot' }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { text: input, sender: 'user' as const }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: input }),
      });

      const data = await res.json();
      const respuesta =
        data?.respuesta_generada ||
        (data?.respuestas_similares?.length
          ? data.respuestas_similares.join('\n')
          : 'No se encontró respuesta.');

      setMessages([...newMessages, { text: respuesta, sender: 'bot' as const }]);
    } catch (err) {
      setMessages([...newMessages, { text: 'Error al conectar con el servidor.', sender: 'bot' as const }]);
    } finally {
      setLoading(false);
    }

  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-purple-50 text-gray-800">
      <div className="flex flex-col w-full max-w-2xl h-[90vh] bg-white rounded-lg shadow-lg overflow-hidden border border-purple-200">
        <header className="bg-purple-200 py-4 text-center text-xl font-semibold text-purple-800">
          Chat de Opiniones por Sucursal
        </header>

        <main className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-3 rounded-lg max-w-[80%] whitespace-pre-wrap ${msg.sender === 'user'
                  ? 'bg-purple-300 self-end ml-auto text-right'
                  : 'bg-purple-100 self-start text-left'
                }`}
            >
              {msg.text}
            </div>
          ))}
          {loading && <p className="text-purple-500">Cargando...</p>}
        </main>

        <footer className="p-4 bg-purple-100 border-t border-purple-200">
          <div className="flex gap-2">
            <input
              className="flex-1 p-2 rounded border border-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu pregunta aquí..."
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="bg-purple-400 hover:bg-purple-500 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              Enviar
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}
