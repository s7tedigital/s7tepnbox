from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# ============================================================
# MÓDULO 1: CLIENTE & MERCADO
# ============================================================

class CriterioSegmentacao(BaseModel):
    """Nota de 0 a 10 para cada um dos 5 critérios de segmentação."""
    tamanho_mercado: float = Field(description="Nota (0-10): Tamanho do segmento")
    margem_lucro: float = Field(description="Nota (0-10): Potencial de lucro")
    tendencia_crescimento: float = Field(description="Nota (0-10): Tendência de crescimento do segmento")
    nivel_concorrencia: float = Field(description="Nota (0-10): Nível de concorrência (10 = pouca)")
    aderencia_solucao: float = Field(description="Nota (0-10): Aderência à solução proposta")
    nota_total: float = Field(description="Soma das 5 notas. Máximo 50.")

class Segmentacao(BaseModel):
    segmento_principal: str = Field(description="Nome e descrição do segmento principal escolhido")
    segmento_secundario: str = Field(description="Nome e descrição do segmento secundário")
    criterios_principal: CriterioSegmentacao = Field(description="Notas do segmento principal")
    criterios_secundario: CriterioSegmentacao = Field(description="Notas do segmento secundário")
    justificativa: str = Field(description="Justificativa da escolha do segmento principal")

class Demographics(BaseModel):
    idade: str = Field(description="Faixa etária (ex: 35-50 anos)")
    genero: str = Field(description="Gênero predominante")
    renda: str = Field(description="Faixa de renda (ex: R$ 5k - 10k)")
    localizacao: str = Field(description="Localização geográfica detalhada")
    escolaridade: str = Field(description="Nível de instrução")

class PersonaRoutine(BaseModel):
    morning: str = Field(description="Rotina detalhada do período da manhã")
    afternoon: str = Field(description="Rotina detalhada do período da tarde")
    night: str = Field(description="Rotina detalhada do período da noite")

class EmotionalSocialBenefits(BaseModel):
    emocionais: List[str] = Field(description="Ganhos emocionais (ex: paz de espírito, confiança)")
    sociais: List[str] = Field(description="Ganhos sociais (ex: status, reconhecimento)")
    funcionais: List[str] = Field(description="Ganhos funcionais (ex: economia de tempo, facilidade)")

class Persona(BaseModel):
    nome_ficticio: str = Field(description="Nome fictício (ex: 'Ricardo Silva')")
    persona_bio: str = Field(description="Biografia longa e detalhada da persona (mínimo 2 parágrafos)")
    demographics: Demographics = Field(description="Dados demográficos estruturados")
    digital_fluency: str = Field(description="Nível de fluência e principais canais (ex: 'Alta: WhatsApp, LinkedIn')")
    routine: PersonaRoutine = Field(description="Rotina diária dividida em 3 períodos")
    dores_principais: List[str] = Field(description="Pores e frustrações principais")
    desejos: List[str] = Field(description="Desejos e aspirações")
    benefits: EmotionalSocialBenefits = Field(description="Benefícios categorizados (Emocionais, Sociais, Funcionais)")
    frase_marcante: str = Field(description="A frase que define a persona")

class CustomerJourneyPhase(BaseModel):
    phase_name: str = Field(description="Nome da fase: Before, During ou After")
    customer_action: str = Field(description="O que o cliente faz nesta fase")
    touchpoints: List[str] = Field(description="Pontos de contato com a marca/solução")
    emotional_state: str = Field(description="Estado emocional do cliente")
    opportunities: List[str] = Field(description="Oportunidades de conversão ou melhoria")

class ClienteMercado(BaseModel):
    tam_sam_som: str = Field(description="Análise quantitativa do mercado brasileiro")
    segmentacao: Segmentacao = Field(description="Matriz de segmentação")
    persona: Persona = Field(description="Perfil ultra-denso da Persona")
    customer_journey: List[CustomerJourneyPhase] = Field(description="Jornada do cliente em 3 fases (Antes, Durante, Depois)")

# ============================================================
# MÓDULO 2: PROBLEMA & SOLUÇÃO
# ============================================================

class PropostaValor(BaseModel):
    declaracao: str = Field(description="Declaração de valor impactante")
    problema_central: str = Field(description="O problema 'dor de cabeça' que resolve")
    solucao_proposta: str = Field(description="A solução e como ela resolve o problema")
    diferenciais_unicos: List[str] = Field(description="Por que somos melhores que o 'status quo'")

class CompetitorMatrixItem(BaseModel):
    name: str = Field(description="Nome do concorrente")
    convenience: float = Field(description="Nota 1-10: Conveniência")
    innovation: float = Field(description="Nota 1-10: Inovação")
    price: float = Field(description="Nota 1-10: Preço (10 = mais competitivo)")
    quality: float = Field(description="Nota 1-10: Qualidade")
    support: float = Field(description="Nota 1-10: Suporte")
    technology: float = Field(description="Nota 1-10: Tecnologia")
    average_score: float = Field(description="Média das notas")

class AnaliseConcorrencia(BaseModel):
    competitor_matrix: List[CompetitorMatrixItem] = Field(description="Matriz comparativa com 2 concorrentes reais + o seu negócio")
    estrategia_defensiva: str = Field(description="Como vamos nos diferenciar e nos proteger no mercado")

class ProblemaSolucao(BaseModel):
    proposta_valor: PropostaValor = Field(description="Mapeamento da Proposta de Valor")
    analise_concorrencia: AnaliseConcorrencia = Field(description="Análise da concorrência e diferencial")

# ============================================================
# MÓDULO 3: ESTRATÉGIA (SWOT EXPANDIDA)
# ============================================================

class ItemSWOT(BaseModel):
    descricao: str = Field(description="Descrição do fator (Força, Fraqueza, etc.)")
    impact_level: str = Field(description="Nível de Impacto: High ou Low")
    strategic_action: str = Field(description="Ação estratégica concreta")

class MatrizSWOTExpandida(BaseModel):
    forcas: List[ItemSWOT]
    fraquezas: List[ItemSWOT]
    oportunidades: List[ItemSWOT]
    ameacas: List[ItemSWOT]

class Estrategia(BaseModel):
    missao: str
    visao: str
    valores: List[str]
    pilares_culturais: str = Field(description="Como a cultura suporta a estratégia")
    swot: MatrizSWOTExpandida = Field(description="SWOT com impacto e ações")
    objetivos_smart: List[str] = Field(description="5 metas claras para o primeiro ano")

# ============================================================
# MÓDULO 4: MARKETING & VENDAS (GROWTH)
# ============================================================

class SalesFunnelStage(BaseModel):
    stage_name: str = Field(description="Stage: Top, Middle ou Bottom")
    description: str = Field(description="O que acontece nesta etapa (AIDA)")
    invested_budget: float = Field(description="Orçamento investido na etapa (R$)")
    reached_people: int = Field(description="Pessoas alcançadas")
    call_to_action_people: int = Field(description="Pessoas que realizaram o CTA")
    cac: float = Field(description="CAC específico da etapa")
    conversion_rate: float = Field(description="Taxa de conversão (%)")

class SalesFunnel(BaseModel):
    top: SalesFunnelStage
    middle: SalesFunnelStage
    bottom: SalesFunnelStage
    global_cac: float
    ltv: float
    ltv_cac_ratio: float

class ExperimentHypothesis(BaseModel):
    hypothesis_description: str
    validation_method: str
    success_metric: str
    deadline: int = Field(description="Prazo em dias")
    status: str = Field(description="Status: Pendente, Validado, Invalidado")

class MarketingPlan(BaseModel):
    sales_funnel: SalesFunnel = Field(description="Funil de vendas detalhado AIDA")
    experiment_board: List[ExperimentHypothesis] = Field(description="Quadro de experimentação")

# ============================================================
# MÓDULO 5: FINANÇAS (DRE 12 MESES)
# ============================================================

class FinancialInvestment(BaseModel):
    item: str
    value: float

class FinancialScenario(BaseModel):
    scenario_name: str = Field(description="Optimistic, Pessimistic ou Probable")
    estimated_revenue: float
    estimated_profit: float
    justification: str

class DREMonth(BaseModel):
    month_name: str = Field(description="Mês (ex: Mês 1)")
    revenue: float = Field(description="Receita Bruta")
    taxes: float = Field(description="Impostos")
    variable_costs: float = Field(description="Custos Variáveis")
    contribution_margin: float = Field(description="Margem de Contribuição")
    fixed_costs: float = Field(description="Custos Fixos")
    net_profit: float = Field(description="Lucro Líquido")

class FinancialPlan(BaseModel):
    fixed_investments: List[FinancialInvestment]
    pre_operational_investments: List[FinancialInvestment]
    working_capital: float
    dre_12_months: List[DREMonth] = Field(description="Projeção mês a mês por um ano")
    scenarios: List[FinancialScenario] = Field(description="Cenários: Otimista, Pessimista, Provável")
    viability_indicators: Dict[str, float] = Field(description="ROI, Payback, Break-even, Lucratividade")
    comentarios_financeiros: str = Field(description="Análise narrativa densa")

# ============================================================
# MÓDULO 6: OPERAÇÕES
# ============================================================

class PlanoOperacional(BaseModel):
    atividades_chaves: List[str]
    parceiros_chaves: List[str]
    infraestrutura: str
    aspectos_legais: str
    quadro_equipe: List[str]

# ============================================================
# MASTER SCHEMA: S7teBusinessPlanV2
# ============================================================

class S7teBusinessPlanV3(BaseModel):
    """Schema Master V3.0 - Padrão SEBRAE PNBOX High Density."""
    sumario_executivo: str = Field(description="Resumo executivo denso e estratégico (Benchmark: CÍTTRICA IA)")
    cliente_mercado: ClienteMercado
    problema_solucao: ProblemaSolucao
    estrategia: Estrategia
    marketing: MarketingPlan
    financas: FinancialPlan
    operacional: PlanoOperacional
