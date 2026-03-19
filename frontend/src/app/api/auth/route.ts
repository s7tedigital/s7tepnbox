import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';
import { createClient } from '@supabase/supabase-js';

const getSupabase = () => {
  let url = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost:54321';
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'dummy_key';
  
  // Auto-fix missing protocol
  if (url && !url.startsWith('http')) {
    url = `https://${url}`;
  }
  
  try {
    return createClient(url, key);
  } catch (e) {
    console.error("Supabase Init Error:", e);
    throw e;
  }
};

export async function POST(request: Request) {
  console.log("Auth API triggered...");
  const hasSecret = !!process.env.SESSION_SECRET;
  console.log("Session Secret configured:", hasSecret);
  
  try {
    const supabase = getSupabase();
    const body = await request.json();
    const { email, password, action } = body;
    console.log(`Action: ${action}, Email: ${email}`);
    
    let authRes;
    if (action === 'register') {
      console.log("Calling supabase.auth.signUp...");
      authRes = await supabase.auth.signUp({ email, password });
    } else {
      console.log("Calling supabase.auth.signInWithPassword...");
      authRes = await supabase.auth.signInWithPassword({ email, password });
    }

    if (authRes.error) {
      console.error("Supabase Auth Error:", authRes.error.message);
      return NextResponse.json({ error: authRes.error.message }, { status: 400 });
    }

    console.log("Auth success. User ID:", authRes.data.user?.id);

    const response = NextResponse.json({ success: true });

    if (authRes.data.user) {
      console.log("Saving session to response cookies...");
      try {
        // We set the session on the RESPONSE cookies specifically so the Set-Cookie header is included
        const session = await getSession(response.cookies);
        session.userId = authRes.data.user.id;
        session.email = authRes.data.user.email;
        session.isLoggedIn = true;
        await session.save();
        console.log("Session saved to response successfully.");
      } catch (sessionErr: any) {
        console.error("Critical Session Error:", sessionErr.message);
        return NextResponse.json({ 
          success: false, 
          error: "Erro ao salvar sessão: " + sessionErr.message 
        }, { status: 500 });
      }
    }

    return response;
  } catch (error: any) {
    console.error("Auth API Crash (Outer):", error);
    return NextResponse.json({ 
      error: error.message || "Internal Server Error",
      stack: error.stack
    }, { status: 500 });
  }
}
