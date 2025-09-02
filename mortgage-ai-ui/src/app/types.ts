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
  lender_categories: {
    major_banks: string[];
    building_societies: string[];
    specialist_lenders: string[];
    other_banks: string[];
  };
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
