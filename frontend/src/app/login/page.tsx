import { LoginForm } from "@/components/auth/login-form";
import Link from "next/link";
import { getSession } from "@/lib/session";
import { redirect } from "next/navigation";

export default async function LoginPage() {
  console.log("Rendering LoginPage...");
  try {
    const session = await getSession();
    console.log("Session status:", session.isLoggedIn ? "LoggedIn" : "LoggedOut");
    if (session.isLoggedIn) redirect("/dashboard");
  } catch (error) {
    console.error("Session Error in LoginPage:", error);
    // Continue rendering the login form even if session retrieval fails
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-zinc-950 text-white p-4">
      <div className="w-full max-w-md p-8 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-2 tracking-tighter">Login</h1>
        <p className="text-zinc-400 text-sm mb-6 text-center">Acesse o seu consultor S7te Digital.</p>
        <LoginForm mode="login" />
        <p className="mt-6 text-sm text-zinc-500">
          Não tem uma conta?{" "}
          <Link href="/register" className="text-white hover:underline">
            Criar conta
          </Link>
        </p>
      </div>
    </div>
  );
}
