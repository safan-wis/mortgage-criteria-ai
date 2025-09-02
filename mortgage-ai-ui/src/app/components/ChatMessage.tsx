import { ChatMessage as ChatMessageType } from '../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`py-6 ${isUser ? 'bg-transparent' : 'bg-transparent'}`}>
      <div className="max-w-5xl mx-auto flex space-x-6">
        {/* Avatar */}
        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg ${
          isUser 
            ? 'bg-gradient-to-br from-blue-500 to-blue-600' 
            : 'bg-gradient-to-br from-indigo-500 to-purple-600'
        }`}>
          <span className="text-white text-lg font-bold">
            {isUser ? 'U' : 'AI'}
          </span>
        </div>
        
        {/* Message Content */}
        <div className="flex-1 space-y-3">
          <div className="text-sm font-semibold" style={{ color: '#111827' }}>
            {isUser ? 'You' : 'Mortgage Criteria AI'}
          </div>
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/30 hover:shadow-2xl transition-all duration-300">
            <div className="prose prose-lg max-w-none">
              <div className="whitespace-pre-wrap leading-relaxed font-normal text-lg" style={{ color: '#1F2937' }}>
                {message.content}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
