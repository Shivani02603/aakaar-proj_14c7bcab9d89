'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

function SessionSidebar({ onSelectSession, activeSessionId }: { onSelectSession: (id: string) => void; activeSessionId?: string }) {
  // Placeholder for SessionSidebar implementation
  return (
    <div className="p-4 border-r border-gray-200">
      <h2 className="text-lg font-semibold mb-4">Sessions</h2>
      {/* Example session list */}
      <ul>
        <li
          className={`cursor-pointer p-2 ${activeSessionId === '1' ? 'bg-blue-100' : ''}`}
          onClick={() => onSelectSession('1')}
        >
          Session 1
        </li>
        <li
          className={`cursor-pointer p-2 ${activeSessionId === '2' ? 'bg-blue-100' : ''}`}
          onClick={() => onSelectSession('2')}
        >
          Session 2
        </li>
      </ul>
    </div>
  );
}

function DocumentUploader() {
  // Placeholder for DocumentUploader implementation
  return (
    <div className="p-4 border-t border-gray-200">
      <h2 className="text-lg font-semibold mb-4">Upload Documents</h2>
      <button className="bg-blue-500 text-white px-4 py-2 rounded">Upload</button>
    </div>
  );
}

function ChatWindow({ activeSessionId }: { activeSessionId?: string }) {
  // Placeholder for ChatWindow implementation
  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4">Chat Window</h2>
      {activeSessionId ? (
        <p>Active Session ID: {activeSessionId}</p>
      ) : (
        <p>Please select a session to start chatting.</p>
      )}
    </div>
  );
}

export default function ChatPage() {
  const router = useRouter();
  const [activeSessionId, setActiveSessionId] = useState<string | undefined>(undefined);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex items-center justify-between bg-gray-800 text-white px-4 py-2">
        <h1 className="text-xl font-bold">Aakaar Project</h1>
        <button onClick={handleLogout} className="bg-red-500 px-4 py-2 rounded">
          Logout
        </button>
      </div>
      <div className="flex flex-1">
        <div className="w-64 bg-gray-100">
          <SessionSidebar
            onSelectSession={(id) => setActiveSessionId(id)}
            activeSessionId={activeSessionId}
          />
          <DocumentUploader />
        </div>
        <div className="flex-1 bg-white">
          <ChatWindow activeSessionId={activeSessionId} />
        </div>
      </div>
    </div>
  );
}