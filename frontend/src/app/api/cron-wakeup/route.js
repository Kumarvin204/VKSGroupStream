import { NextResponse } from 'next/server';

export async function GET(request) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';
    const healthUrl = `${backendUrl}/api/health`;

    console.log(`Cron wake-up triggered. Pinging backend at: ${healthUrl}`);
    
    const response = await fetch(healthUrl, {
      method: 'GET',
      headers: {
        'Cache-Control': 'no-cache',
      },
      next: { revalidate: 0 } // Prevent Next.js from caching the fetch request
    });

    if (!response.ok) {
      throw new Error(`Backend health check failed with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json({ success: true, message: 'Backend successfully woken up', data });
  } catch (error) {
    console.error('Error in cron wake-up:', error.message);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
