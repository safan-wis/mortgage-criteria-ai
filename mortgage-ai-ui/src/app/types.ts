export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface SearchResult {
  text: string;
  metadata: {
    lender_name: string;
    criteria_section: string;
    filename: string;
    chunk_index?: number;
  };
  score?: number;
}

export interface LenderConfig {
  total_lenders: number;
  total_chunks: number;
  lenders: string[];
  last_updated: string;
}

export interface SearchRequest {
  query: string;
  lender_filter?: string;
  num_results?: number;
}

export interface ChatRequest {
  messages: ChatMessage[];
  query: string;
  lender_filter?: string;
  num_results?: number;
}

export interface ChatResponse {
  response: string;
  search_results: SearchResult[];
}
