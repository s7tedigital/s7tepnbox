import { getSession } from "@/lib/session";
import { redirect } from "next/navigation";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default async function DashboardPage() {
  const session = await getSession();
  
  if (!session.isLoggedIn) {
    redirect("/login");
  }

  const newPlanId = "new-plan";

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <header className="flex justify-between items-center mb-12 border-b border-zinc-800 pb-4">
        <h1 className="text-2xl font-bold tracking-tighter">S7te Dashboard</h1>
        <p className="text-zinc-400 text-sm">Logado como: {session.email}</p>
      </header>
      
      <main className="max-w-4xl mx-auto flex flex-col gap-6">
        <div className="p-6 bg-zinc-900 border border-zinc-800 rounded-xl flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">Novo Plano de Negócios</h2>
            <p className="text-zinc-400 text-sm">Inicie uma consultoria de 15 minutos com a nossa IA audaz.</p>
          </div>
          <Link href={`/builder/${newPlanId}`}>
            <Button size="lg">Iniciar Consultoria</Button>
          </Link>
        </div>
        
        <div className="mt-8">
          <h3 className="text-lg font-medium mb-4 text-zinc-300">Meus Planos Recentes</h3>
          <div className="p-8 text-center border border-dashed border-zinc-800 rounded-xl text-zinc-500">
            Você ainda não possui nenhum plano gerado.
          </div>
        </div>
      </main>
    </div>
  );
}
