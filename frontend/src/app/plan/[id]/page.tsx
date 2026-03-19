"use client";

import { FinancialOverview, FinancialProjection } from "@/components/dashboard/charts";
import { BrainCircuit, Download, Lock, CheckCircle2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

// Mock Data corresponding to a realistic output from the Financial Engineer Gemini Node
const mockFinancials: FinancialProjection = {
    initial_investment_total: 15500,
    monthly_fixed_costs: 4200,
    expected_monthly_revenue: 12000,
    break_even_point_months: 2.1,
    roi_percentage: 450.5,
    costs_breakdown: [
        { name: "Licenças de Software Premium", amount: 1500, type: "investimento_inicial" },
        { name: "Identidade Visual e Branding", amount: 3000, type: "investimento_inicial" },
        { name: "MacBook Pro M3", amount: 11000, type: "investimento_inicial" },
        { name: "Tráfego Pago Mensal", amount: 2000, type: "variavel" },
        { name: "Contabilidade e Taxas", amount: 800, type: "fixa" },
        { name: "Infraestrutura Cloud VPS", amount: 400, type: "fixa" },
        { name: "Pró-labore Mínimo", amount: 1000, type: "fixa" }
    ]
};

export default function PlanDashboardPage({ params }: { params: { id: string } }) {
  // Num cenário real, buscaríamos isso do Supabase (isPaid) no SSR ou via hook
  const [isPaid, setIsPaid] = useState(false);
  const [isProcessingCheckout, setIsProcessingCheckout] = useState(false);
  const planId = params.id || "MVP-001";

  const handleCheckout = async () => {
      setIsProcessingCheckout(true);
      try {
          const res = await fetch(`/api/v1/stripe/create-checkout-session?plan_id=${planId}`, {
              method: 'POST'
          });
          if (res.ok) {
              const data = await res.json();
              if (data.checkout_url) {
                  window.location.href = data.checkout_url;
              }
          }
      } catch (error) {
          console.error("Erro ao iniciar checkout", error);
      } finally {
          setIsProcessingCheckout(false);
      }
  };

  const downloadPdfUrl = `/api/v1/plans/${planId}/pdf`;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 font-sans pb-24 relative">
       {/* Premium Header */}
       <header className="h-16 border-b border-zinc-800/60 bg-zinc-900/50 backdrop-blur-md sticky top-0 z-20 flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500 to-emerald-500 rounded-lg shadow-lg shadow-emerald-500/10">
            <BrainCircuit className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-zinc-100 tracking-tight">Executive Dashboard</h1>
            <p className="text-xs text-zinc-400 font-medium">Plan #{planId}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
            {isPaid ? (
                <a href={downloadPdfUrl} target="_blank" rel="noopener noreferrer">
                    <Button variant="outline" className="border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10 hover:text-emerald-300">
                        <Download className="w-4 h-4 mr-2" /> Baixar PDF Executivo
                    </Button>
                </a>
            ) : (
                <Button 
                    onClick={handleCheckout} 
                    disabled={isProcessingCheckout}
                    className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white border-0 shadow-lg shadow-emerald-500/20"
                >
                    <Lock className="w-4 h-4 mr-2" /> {isProcessingCheckout ? "Processando..." : "Liberar Plano Completo"}
                </Button>
            )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 pt-12 relative z-10">
         {/* Executive Summary */}
         <div className="mb-12">
            <h2 className="text-4xl font-bold tracking-tight mb-4 bg-gradient-to-r from-zinc-100 to-zinc-400 bg-clip-text text-transparent">
                Agência de Inteligência Artificial Local
            </h2>
            <div className="p-6 bg-indigo-500/5 border border-indigo-500/20 rounded-2xl relative overflow-hidden">
                 <h3 className="text-lg font-semibold text-indigo-300 mb-2">Resumo Executivo do Consultor IA</h3>
                 <p className="text-zinc-400 leading-relaxed">
                     Esta ideia apresenta altíssima viabilidade técnica e financeira. O investimento inicial é focado em CAPEX (equipamentos) e branding, com baixo custo operacional mensal graças ao modelo remoto. A alta margem dos serviços...
                 </p>
                 
                 {!isPaid && (
                     <div className="absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-zinc-950 to-transparent pointer-events-none"></div>
                 )}
            </div>
         </div>

         {/* Financial Interactive Dashboard with PAYWALL */}
         <div className="relative">
             <div className="space-y-4 mb-8">
                 <h3 className="text-2xl font-semibold tracking-tight">Projeção Financeira Realista</h3>
                 <p className="text-zinc-500">Engenharia reversa calculada automaticamente com base nos seus dados.</p>
             </div>

             <div className={!isPaid ? "filter blur-md select-none pointer-events-none opacity-40 transition-all duration-500" : ""}>
                 <FinancialOverview data={mockFinancials} />
             </div>

             {/* Web3 Paywall Modal Style */}
             {!isPaid && (
                 <div className="absolute inset-0 z-10 flex flex-col items-center justify-center pt-32 pb-16">
                     <div className="max-w-md w-full bg-zinc-900/90 backdrop-blur-xl border border-zinc-800 p-8 rounded-3xl shadow-2xl text-center transform hover:scale-[1.02] transition-transform duration-300">
                         <div className="mx-auto w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mb-6 border border-emerald-500/20">
                             <Lock className="w-8 h-8 text-emerald-400" />
                         </div>
                         <h3 className="text-2xl font-bold text-white mb-2">Desbloqueie seu Plano</h3>
                         <p className="text-zinc-400 mb-8 leading-relaxed">
                             O plano completo inclui detalhamento visual de DRE, ROI, e exportação do PDF Executivo gerado pela nossa IA.
                         </p>
                         
                         <div className="space-y-3 mb-8 text-left text-sm text-zinc-300">
                             <div className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-500"/> PDF Executivo Imediato</div>
                             <div className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-500"/> Gráficos Interativos de DRE</div>
                             <div className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-500"/> Estruturação Validada</div>
                         </div>

                         <Button 
                            onClick={handleCheckout} 
                            disabled={isProcessingCheckout}
                            className="w-full h-12 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl text-lg flex items-center justify-center group"
                         >
                             {isProcessingCheckout ? "Aguarde..." : (
                                 <>Via Pagamento Seguro <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" /></>
                             )}
                         </Button>
                         <p className="text-xs text-zinc-500 mt-4 flex items-center justify-center gap-1">
                             <Lock className="w-3 h-3"/> Checkout Seguro via Stripe
                         </p>
                     </div>
                 </div>
             )}
         </div>

      </main>
    </div>
  );
}
