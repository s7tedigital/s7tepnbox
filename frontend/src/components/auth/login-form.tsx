"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export function LoginForm({ mode }: { mode: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    console.log("Submitting auth form...");
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 20000); // 20s timeout

    try {
      const res = await fetch("/api/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, action: mode }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      console.log("Fetch response status:", res.status);
      const data = await res.json();
      console.log("Fetch response data:", data);
      setLoading(false);

      if (data.error) {
        setError(data.error);
        if (data.stack) console.error("Server Stack:", data.stack);
      } else {
        console.log("Redirecting to dashboard...");
        router.push("/dashboard");
      }
    } catch (err: any) {
      clearTimeout(timeoutId);
      setLoading(false);
      console.error("Login Fetch Error:", err);
      if (err.name === 'AbortError') {
        setError("O servidor demorou muito para responder (Timeout). Verifique sua conexão ou tente novamente.");
      } else {
        setError("Erro ao conectar ao servidor: " + err.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4 w-full max-w-sm">
      <div className="flex flex-col space-y-2">
        <label className="text-sm font-medium text-zinc-300">Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="flex h-10 w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-400"
          required
        />
      </div>
      <div className="flex flex-col space-y-2">
        <label className="text-sm font-medium text-zinc-300">Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="flex h-10 w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-400"
          required
        />
      </div>
      {error && <p className="text-sm text-red-500">{error}</p>}
      <Button type="submit" disabled={loading} className="w-full mt-4">
        {loading ? "Processando..." : mode === "login" ? "Entrar" : "Criar Conta"}
      </Button>
    </form>
  );
}
