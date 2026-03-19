import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-zinc-950 text-white">
      <h1 className="text-4xl font-bold mb-4 tracking-tighter">S7te Plan Builder</h1>
      <p className="text-zinc-400 mb-8 max-w-md text-center">
        O seu plano de negócios construído em 15 minutos por um consultor IA audaz.
      </p>
      <Link href="/login">
        <Button variant="default" size="lg">Iniciar Discovery</Button>
      </Link>
    </div>
  );
}
