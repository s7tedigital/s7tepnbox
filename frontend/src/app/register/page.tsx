import { LoginForm } from "@/components/auth/login-form";
import Link from "next/link";
import { getSession } from "@/lib/session";
import { redirect } from "next/navigation";

export default async function RegisterPage() {
  console.log("Rendering RegisterPage...");
  try {
    const session = await getSession();
    console.log("Session status:", session.isLoggedIn ? "LoggedIn" : "LoggedOut");
    if (session.isLoggedIn) redirect("/dashboard");
  } catch (error) {
    console.error("Session Error in RegisterPage:", error);
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-zinc-950 text-white p-4">
      <div className="w-full max-w-md p-8 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-2 tracking-tighter">Criar Conta</h1>
        <p className="text-zinc-400 text-sm mb-6 text-center">Inicie a sua jornada com o S7te Plan Builder.</p>
        <LoginForm mode="register" />
        <p className="mt-6 text-sm text-zinc-500">
          Já tem conta?{" "}
          <Link href="/login" className="text-white hover:underline">
            Entrar
          </Link>
        </p>
      </div>
    </div>
  );
}
