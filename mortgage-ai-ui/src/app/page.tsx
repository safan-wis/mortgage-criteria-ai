'use client';

import { useState, useRef, useEffect } from 'react';
import ChatMessage from './components/ChatMessage';
import Sidebar from './components/Sidebar';
import { ChatMessage as ChatMessageType, SearchResult } from './types';

export default function Home() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLender, setSelectedLender] = useState('All Lenders');
  const [numResults, setNumResults] = useState(15);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (query?: string) => {
    const messageText = query || input;
    if (!messageText.trim() || isLoading) return;

    const userMessage: ChatMessageType = { role: 'user', content: messageText };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage],
          query: messageText,
          lender_filter: selectedLender === 'All Lenders' ? undefined : selectedLender,
          num_results: numResults,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      const assistantMessage: ChatMessageType = { 
        role: 'assistant', 
        content: data.response 
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      setSearchResults(data.search_results || []);
      
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessageType = { 
        role: 'assistant', 
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}` 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleQuery = (query: string) => {
    setInput(query);
    handleSend(query);
  };

  const handleClearChat = () => {
    setMessages([]);
    setSearchResults([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const adjustTextareaHeight = () => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 200)}px`;
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [input]);

  const toggleSidebarCollapse = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50" style={{ color: '#111827' }}>
      {/* Mobile Sidebar Toggle */}
      <div className="lg:hidden fixed top-6 left-6 z-50">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-3 bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 text-gray-700 hover:text-gray-900 hover:bg-white transition-all duration-300 hover:scale-105"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 fixed lg:static inset-y-0 left-0 z-40 transition-transform duration-300 ease-in-out`}>
        <Sidebar
          selectedLender={selectedLender}
          setSelectedLender={setSelectedLender}
          numResults={numResults}
          setNumResults={setNumResults}
          onExampleQuery={handleExampleQuery}
          onClearChat={handleClearChat}
          isCollapsed={sidebarCollapsed}
          onToggleCollapse={toggleSidebarCollapse}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col lg:ml-0">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-md border-b border-white/20 px-8 py-6 shadow-lg">
          <div className="flex items-center justify-between max-w-6xl mx-auto">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl flex items-center justify-center shadow-lg">
                <span className="text-2xl text-white font-bold">🏦</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-800 bg-clip-text text-transparent">
                  Mortgage Criteria AI
                </h1>
                <p className="text-sm font-medium" style={{ color: '#6B7280' }}>
                  Expert guidance across 30+ UK lenders
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleClearChat}
                className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100/80 rounded-xl transition-all duration-200 hover:shadow-md"
              >
                Clear Chat
              </button>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          <div className="max-w-5xl mx-auto">
            {messages.length === 0 && (
              <div className="text-center py-16">
                <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-3xl flex items-center justify-center shadow-xl">
                  <span className="text-4xl">🏦</span>
                </div>
                <h3 className="text-2xl font-bold mb-3 bg-gradient-to-r from-gray-900 to-blue-800 bg-clip-text text-transparent">
                  Welcome to Mortgage Criteria AI
                </h3>
                <p className="text-lg mb-8" style={{ color: '#6B7280' }}>
                  Get instant, accurate answers about UK mortgage lender criteria
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                  {[
                    "What's the maximum age for mortgage applications?",
                    "LTV limits for first time buyers",
                    "Income requirements for self employed",
                    "Minimum deposit requirements"
                  ].map((query, index) => (
                    <button
                      key={index}
                      onClick={() => handleExampleQuery(query)}
                      className="p-4 text-sm text-left bg-white/80 backdrop-blur-sm border border-white/30 rounded-2xl hover:bg-white hover:border-blue-200 hover:shadow-xl transition-all duration-300 hover:scale-105 group"
                      style={{ color: '#374151' }}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                          </svg>
                        </div>
                        <span className="font-medium">{query}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}

            {isLoading && (
              <div className="flex items-center justify-center py-8">
                <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/30">
                  <div className="flex items-center space-x-4">
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full animate-bounce"></div>
                      <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-sm font-medium" style={{ color: '#6B7280' }}>
                      Searching mortgage criteria...
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-white/20 bg-white/80 backdrop-blur-md px-6 py-6 shadow-lg">
          <div className="max-w-5xl mx-auto">
            <div className="relative">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about mortgage criteria..."
                className="w-full p-5 pr-20 border border-white/30 rounded-2xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-400 resize-none bg-white/90 backdrop-blur-sm shadow-lg text-lg"
                rows={1}
                disabled={isLoading}
                style={{ 
                  minHeight: '64px',
                  color: '#111827'
                }}
              />
              <button
                onClick={() => handleSend()}
                disabled={isLoading || !input.trim()}
                className="absolute right-3 bottom-3 p-3 bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-xl hover:from-blue-700 hover:to-indigo-800 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-300 hover:scale-105 hover:shadow-lg shadow-md"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <p className="text-xs mt-3 text-center" style={{ color: '#9CA3AF' }}>
              Press Enter to send, Shift+Enter for new line
            </p>
          </div>
        </div>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
