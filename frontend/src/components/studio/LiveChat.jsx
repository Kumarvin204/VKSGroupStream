'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';

export default function LiveChat({ liveChatId }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isPolling, setIsPolling] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!liveChatId) return;

    let timeoutId;
    let isMounted = true;

    const pollChat = async () => {
      try {
        setIsPolling(true);
        // Using real YouTube API proxy endpoint
        const res = await fetch(`/api/youtube/chat/${liveChatId}`);
        if (!res.ok) throw new Error('Failed to fetch chat');
        
        const data = await res.json();
        
        if (isMounted) {
          if (data.items) {
            setMessages(prev => {
              // Simple deduplication logic could go here
              return [...prev, ...data.items];
            });
          }
          
          // Use polling interval from YouTube or default to 5s
          const pollInterval = data.pollingIntervalMillis || 5000;
          timeoutId = setTimeout(pollChat, pollInterval);
        }
      } catch (error) {
        console.error('Failed to poll chat:', error);
        if (isMounted) {
          timeoutId = setTimeout(pollChat, 10000); // Retry after 10s on error
        }
      }
    };

    pollChat();

    return () => {
      isMounted = false;
      clearTimeout(timeoutId);
    };
  }, [liveChatId]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Optimistic update
    const optimisticMessage = {
      id: Date.now().toString(),
      authorDetails: {
        displayName: 'Studio Host',
        profileImageUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Host'
      },
      snippet: {
        displayMessage: inputValue
      }
    };

    setMessages(prev => [...prev, optimisticMessage]);
    setInputValue('');
    
    try {
      await fetch(`/api/youtube/chat/${liveChatId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: optimisticMessage.snippet.displayMessage })
      });
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="p-4 bg-slate-800 border-b border-slate-700 flex items-center justify-between">
        <h3 className="text-white font-semibold flex items-center gap-2">
          Live Chat
          {isPolling && <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />}
        </h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-500 text-sm">
            No messages yet. Say hello!
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className="flex gap-3">
              <img 
                src={msg.authorDetails?.profileImageUrl || 'https://api.dicebear.com/7.x/avataaars/svg?seed=fallback'} 
                alt={msg.authorDetails?.displayName || 'User'}
                className="w-8 h-8 rounded-full bg-slate-800 flex-shrink-0"
              />
              <div className="flex flex-col">
                <span className="text-slate-400 text-xs font-medium mb-1">
                  {msg.authorDetails?.displayName || 'User'}
                </span>
                <p className="text-slate-200 text-sm break-words">
                  {msg.snippet?.displayMessage}
                </p>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 bg-slate-800 border-t border-slate-700">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
          />
          <button 
            type="submit"
            disabled={!inputValue.trim()}
            className="p-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center justify-center"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
