"use client";

import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

// Types based on the Python Pydantic Schema
export interface CostItem {
  name: string;
  amount: number;
  type: 'fixa' | 'variavel' | 'investimento_inicial';
}

export interface FinancialProjection {
  initial_investment_total: number;
  monthly_fixed_costs: number;
  expected_monthly_revenue: number;
  break_even_point_months: number;
  roi_percentage: number;
  costs_breakdown: CostItem[];
}

const COLORS = ['#6366f1', '#a855f7', '#ec4899', '#14b8a6', '#f59e0b'];

export function FinancialOverview({ data }: { data: FinancialProjection }) {
  const formatBRL = (value: number) => 
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);

  // Prepare data for the Bar Chart (Revenue vs Costs)
  const monthlyData = [
    { name: 'Receita Esperada', valor: data.expected_monthly_revenue, fill: '#10b981' }, // Emerald
    { name: 'Custo Fixo Mensal', valor: data.monthly_fixed_costs, fill: '#ef4444' }, // Red
  ];

  // Prepare data for the Pie Chart (Cost Distribution)
  const pieData = data.costs_breakdown.map(item => ({
    name: item.name,
    value: item.amount
  })).sort((a, b) => b.value - a.value).slice(0, 5); // Top 5 costs

  // Break-even projection (Simulating 12 months)
  const breakEvenData = Array.from({ length: 12 }).map((_, i) => {
     const month = i + 1;
     const accumulatedProfit = (data.expected_monthly_revenue - data.monthly_fixed_costs) * month;
     const debt = data.initial_investment_total - accumulatedProfit;
     return {
         month: `Mês ${month}`,
         saldo: debt > 0 ? -debt : Math.abs(debt),
         isBreakEven: month === Math.ceil(data.break_even_point_months)
     };
  });

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="pb-2">
            <CardDescription className="text-zinc-400">Investimento Inicial</CardDescription>
            <CardTitle className="text-3xl text-zinc-100">{formatBRL(data.initial_investment_total)}</CardTitle>
          </CardHeader>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800 relative overflow-hidden">
             <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl rounded-bl-full"></div>
            <CardHeader className="pb-2">
                <CardDescription className="text-zinc-400">Ponto de Equilíbrio (Break-even)</CardDescription>
                <CardTitle className="text-3xl text-indigo-400">{data.break_even_point_months.toFixed(1)} Meses</CardTitle>
            </CardHeader>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl rounded-bl-full"></div>
          <CardHeader className="pb-2">
            <CardDescription className="text-zinc-400">ROI Estimado Anual</CardDescription>
            <CardTitle className="text-3xl text-emerald-400">{data.roi_percentage.toFixed(1)}%</CardTitle>
          </CardHeader>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Receita x Custo */}
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-100">Projeção Base Mensal</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] w-full mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                  <XAxis dataKey="name" stroke="#a1a1aa" tick={{fill: '#a1a1aa'}} />
                  <YAxis stroke="#a1a1aa" tickFormatter={(value) => `R$${value/1000}k`} />
                     <RechartsTooltip 
                        contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#f4f4f5' }}
                        formatter={(value: any) => formatBRL(value)}
                     />
                  <Bar dataKey="valor" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Top Custos */}
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-100">Distribuição de Custos</CardTitle>
          </CardHeader>
          <CardContent>
             <div className="h-[300px] w-full mt-4">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={80}
                            outerRadius={110}
                            paddingAngle={5}
                            dataKey="value"
                            stroke="none"
                        >
                            {pieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <RechartsTooltip 
                            contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#f4f4f5' }}
                            formatter={(value: any) => formatBRL(value)}
                        />
                        <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                </ResponsiveContainer>
             </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Gráfico Linear de Break Even */}
      <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-100">Curva de Recuperação do Investimento (12 Meses)</CardTitle>
            <CardDescription className="text-zinc-400">Evolução do Saldo de Caixa Projetado</CardDescription>
          </CardHeader>
          <CardContent>
             <div className="h-[300px] w-full mt-4">
               <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={breakEvenData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                     <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                     <XAxis dataKey="month" stroke="#a1a1aa" />
                     <YAxis stroke="#a1a1aa" tickFormatter={(value) => `R$${value/1000}k`} />
                     <RechartsTooltip 
                        contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#f4f4f5' }}
                        formatter={(value: any) => formatBRL(value)}
                     />
                     <Line type="monotone" dataKey="saldo" stroke="#818cf8" strokeWidth={3} dot={{ r: 4, fill: '#818cf8' }} activeDot={{ r: 8 }} />
                  </LineChart>
               </ResponsiveContainer>
             </div>
          </CardContent>
        </Card>
    </div>
  );
}
