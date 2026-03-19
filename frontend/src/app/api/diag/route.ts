import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';
import { cookies } from 'next/headers';

export async function GET() {
  const session = await getSession();
  const cookieStore = await cookies();
  const allCookies = cookieStore.getAll().map(c => ({ name: c.name, value: c.value.substring(0, 10) + '...' }));
  
  return NextResponse.json({
    timestamp: new Date().toISOString(),
    node_env: process.env.NODE_ENV,
    has_session_secret: !!process.env.SESSION_SECRET,
    session_id: session.userId || 'none',
    is_logged_in: session.isLoggedIn || false,
    cookies_present: allCookies,
  });
}
