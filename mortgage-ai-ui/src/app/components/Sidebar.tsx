import { useState, useEffect } from 'react';
import { LenderConfig } from '../types';

interface SidebarProps {
  selectedLender: string;
  setSelectedLender: (lender: string) => void;
  numResults: number;
  setNumResults: (num: number) => void;
  onExampleQuery: (query: string) => void;
  onClearChat: () => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
}

export default function Sidebar({ 
  selectedLender, 
  setSelectedLender, 
  numResults, 
  setNumResults, 
  onExampleQuery,
  onClearChat,
  isCollapsed,
  onToggleCollapse
}: SidebarProps) {
  const [lenders, setLenders] = useState<string[]>([]);
  
  useEffect(() => {
    // Load lender configuration
    const loadLenders = async () => {
      try {
        const response = await fetch('/api/lenders');
        if (response.ok) {
          const config: LenderConfig = await response.json();
          
          // The new API returns clean lender names directly
          const cleanLenders = config.lenders.map(lender => {
            // Additional cleaning if needed
            let name = lender.replace('-.Txt', '').replace('.Txt', '');
            return name.trim();
          });
          
          setLenders(['All Lenders', ...cleanLenders.sort()]);
        }
      } catch (error) {
        console.error('Failed to load lenders:', error);
        // Fallback to hardcoded list
        setLenders([
          'All Lenders',
          'HSBC',
          'Barclays',
          'NatWest',
          'Santander',
          'Halifax',
          'Nationwide',
          'Virgin Money',
          'Metro Bank',
          'Coventry Building Society',
          'Skipton Building Society',
          'Leeds Building Society',
          'Principality Building Society',
          'Newcastle Building Society',
          'Nottingham Building Society',
          'Pepper Money',
          'Accord Mortgages',
          'Fleet Mortgages',
          'KMC Lending',
          'LendInvest',
          'The Mortgage Lender',
          'Vida Home Loans',
          'Moda Mortgages',
          'Kent Reliance',
          'Furness Building Society',
          'Leek Building Society',
          'Scottish Widows',
          'Bank of Ireland',
          'Clydesdale Bank'
        ]);
      }
    };
    
    loadLenders();
  }, []);

  const exampleQueries = [
    "maximum age for mortgage applications",
    "LTV limits for first time buyers", 
    "income requirements for self employed",
    "minimum deposit requirements",
    "foreign national mortgage criteria",
    "buy to let mortgage rules"
  ];

  return (
    <div className={`${isCollapsed ? 'w-20' : 'w-80'} bg-white/90 backdrop-blur-md border-r border-white/30 h-full overflow-hidden shadow-2xl transition-all duration-300 ease-in-out relative`} style={{ color: '#111827' }}>
      
      {/* Collapse Toggle Button - Fixed at top */}
      <div className="absolute top-4 right-4 z-50">
        <button
          onClick={onToggleCollapse}
          className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 flex items-center justify-center border-2 border-white/20"
          title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          <svg 
            className={`w-5 h-5 transition-transform duration-300 ${isCollapsed ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>

      <div className={`p-8 space-y-8 transition-all duration-300 ${isCollapsed ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}>
        {/* Header */}
        <div className="border-b border-white/30 pb-6 pt-12">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-blue-800 bg-clip-text text-transparent">Settings</h2>
          </div>
        </div>

        {/* Search Options */}
        <div className="space-y-6">
          <h3 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#6B7280' }}>Search Options</h3>
          
          {/* Lender Filter */}
          <div>
            <label className="block text-sm font-semibold mb-3" style={{ color: '#374151' }}>
              Lender Filter
            </label>
            <select 
              value={selectedLender}
              onChange={(e) => setSelectedLender(e.target.value)}
              className="w-full p-3 border border-white/30 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-400 text-sm bg-white/80 backdrop-blur-sm shadow-lg transition-all duration-200"
              style={{ color: '#111827' }}
            >
              <option value="All Lenders">All Lenders</option>
              {lenders.map(lender => (
                <option key={lender} value={lender}>{lender}</option>
              ))}
            </select>
          </div>

          {/* Number of Results */}
          <div>
            <label className="block text-sm font-semibold mb-3" style={{ color: '#374151' }}>
              Results: <span className="text-blue-600 font-bold">{numResults}</span>
            </label>
            <input
              type="range"
              min="5"
              max="20"
              value={numResults}
              onChange={(e) => setNumResults(parseInt(e.target.value))}
              className="w-full h-2 bg-gradient-to-r from-blue-200 to-indigo-200 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs mt-2" style={{ color: '#9CA3AF' }}>
              <span>5</span>
              <span>20</span>
            </div>
          </div>
        </div>

        {/* Database Info */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#6B7280' }}>Database</h3>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-2xl border border-blue-100 shadow-lg">
            <div className="text-center">
              <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-700 bg-clip-text text-transparent mb-2">30+</div>
              <div className="text-sm font-medium" style={{ color: '#4B5563' }}>Total Lenders</div>
            </div>
          </div>
        </div>

        {/* Quick Examples */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#6B7280' }}>Quick Examples</h3>
          <div className="space-y-3">
            {exampleQueries.map((query, index) => (
              <button
                key={index}
                onClick={() => onExampleQuery(query)}
                className="w-full text-left p-4 text-sm bg-white/60 backdrop-blur-sm border border-white/40 rounded-xl hover:bg-white hover:border-blue-200 hover:shadow-xl transition-all duration-300 hover:scale-105 group"
                style={{ color: '#374151' }}
              >
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                  <span className="font-medium">{query}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider" style={{ color: '#6B7280' }}>Actions</h3>
          <button
            onClick={onClearChat}
            className="w-full p-4 bg-gradient-to-r from-red-500 to-pink-600 text-white rounded-xl hover:from-red-600 hover:to-pink-700 transition-all duration-300 hover:scale-105 hover:shadow-xl shadow-lg font-semibold text-sm"
          >
            <div className="flex items-center justify-center space-x-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>Clear Chat History</span>
            </div>
          </button>
        </div>
      </div>

      {/* Collapsed State - Show only icons */}
      <div className={`absolute inset-0 flex flex-col items-center justify-center space-y-8 transition-all duration-300 ${isCollapsed ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
        {/* Settings Icon */}
        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg cursor-pointer hover:shadow-xl transition-all duration-300 hover:scale-110">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>

        {/* Database Icon */}
        <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg cursor-pointer hover:shadow-xl transition-all duration-300 hover:scale-110">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
          </svg>
        </div>

        {/* Examples Icon */}
        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center shadow-lg cursor-pointer hover:shadow-xl transition-all duration-300 hover:scale-110">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>

        {/* Clear Chat Icon */}
        <div className="w-12 h-12 bg-gradient-to-r from-red-500 to-pink-600 rounded-2xl flex items-center justify-center shadow-lg cursor-pointer hover:shadow-xl transition-all duration-300 hover:scale-110">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </div>
      </div>
    </div>
  );
}
