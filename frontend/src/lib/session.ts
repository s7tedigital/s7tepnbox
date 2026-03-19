import { getIronSession } from "iron-session";
import { cookies } from "next/headers";

export interface SessionData {
  userId?: string;
  email?: string;
  isLoggedIn: boolean;
}

export const sessionOptions = {
  // Password must be at least 32 characters
  password: process.env.SESSION_SECRET || "s7te_super_secret_session_key_v3_32c",
  cookieName: "s7te_auth_session",
  cookieOptions: {
    // secure: true is absolutely required for sameSite: "lax" in production
    secure: process.env.NODE_ENV === "production",
    httpOnly: true,
    sameSite: "lax" as const,
    path: "/",
  },
};

export async function getSession(customCookies?: any) {
  const cookieStore = customCookies || await cookies();
  return getIronSession<SessionData>(cookieStore, sessionOptions);
}
