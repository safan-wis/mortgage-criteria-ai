import { NextRequest, NextResponse } from 'next/server';
import { ChatRequest, ChatResponse } from '../../types';

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json();
    
    // Use the optimized FastAPI backend
    const backendUrl = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: body.messages,
        query: body.query,
        lender_filter: body.lender_filter,
        num_results: body.num_results || 15,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: `Failed to generate chat response: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500 }
    );
  }
}
