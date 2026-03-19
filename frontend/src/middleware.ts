import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getIronSession } from 'iron-session';
import { sessionOptions, SessionData } from '@/lib/session';

const protectedRoutes = ['/dashboard', '/builder', '/plan'];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  console.log(`Middleware tracking: ${pathname}`);

  // Debug: check for cookie existence before anything else
  const rawCookie = request.cookies.get(sessionOptions.cookieName);
  console.log(`Cookie ${sessionOptions.cookieName} present: ${!!rawCookie}`);

  // Use the request's own cookies for reading session in Middleware (Edge Runtime)
  let session: SessionData = { isLoggedIn: false };
  try {
    session = await getIronSession<SessionData>(request.cookies as any, sessionOptions);
    console.log(`Session decrypted -> isLoggedIn: ${session.isLoggedIn}, UserID: ${session.userId}`);
  } catch (err: any) {
    console.error("Middleware Session Decryption Fail:", err.message);
  }
  
  // Protect specific routes
  const isProtected = protectedRoutes.some(route => pathname.startsWith(route));
  
  if (isProtected && !session.isLoggedIn) {
     console.log(`Access Denied to ${pathname}. Redirecting to /login`);
     return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // Forward to FastAPI API backend injecting the User ID
  if (pathname.startsWith('/api/v1/')) {
      const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
      
      // The Backend only trusts this Header explicitly set by this Proxy Middleware
      const requestHeaders = new Headers(request.headers);
      if (session.userId) {
          requestHeaders.set('X-User-Id', session.userId);
      }
      
      return NextResponse.rewrite(new URL(`${backendUrl}${pathname}`, request.url), {
        request: {
          headers: requestHeaders,
        },
      });
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/builder/:path*', '/plan/:path*', '/api/v1/:path*'],
};
