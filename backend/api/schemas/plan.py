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
    justificativa: str = Field(description="Justificativa técnica longa da escolha do segmento principal (mín 3 parágrafos)")

class Demographics(BaseModel):
    idade: str = Field(description="Faixa etária (ex: 35-50 anos)")
    genero: str = Field(description="Gênero predominante")
    renda: str = Field(description="Faixa de renda (ex: R$ 5k - 10k)")
    localizacao: str = Field(description="Localização geográfica detalhada")
    escolaridade: str = Field(description="Nível de instrução")

class PersonaRoutine(BaseModel):
    morning: str = Field(description="Rotina detalhada do período da manhã (descrição minuciosa)")
    afternoon: str = Field(description="Rotina detalhada do período da tarde (descrição minuciosa)")
    night: str = Field(description="Rotina detalhada do período da noite (descrição minuciosa)")

class EmotionalSocialBenefits(BaseModel):
    emocionais: List[str] = Field(description="Ganhos emocionais com justificativa")
    sociais: List[str] = Field(description="Ganhos sociais com justificativa")
    funcionais: List[str] = Field(description="Ganhos funcionais com justificativa")

class Persona(BaseModel):
    nome_ficticio: str = Field(description="Nome fictício")
    persona_bio: str = Field(description="Biografia ultra-longa e detalhada da persona (mínimo 5 parágrafos)")
    demographics: Demographics = Field(description="Dados demográficos estruturados")
    digital_fluency: str = Field(description="Nível de fluência e principais canais com análise de uso")
    routine: PersonaRoutine = Field(description="Rotina diária dividida em 3 períodos detalhados")
    dores_principais: List[str] = Field(description="Dores e frustrações principais detalhadas")
    desejos: List[str] = Field(description="Desejos e aspirações detalhadas")
    benefits: EmotionalSocialBenefits = Field(description="Benefícios categorizados com análises longas")
    frase_marcante: str = Field(description="A frase que define a persona")

class CustomerJourneyPhase(BaseModel):
    phase_name: str = Field(description="Nome da fase: Before, During ou After")
    customer_action: str = Field(description="O que o cliente faz nesta fase (descrição longa)")
    touchpoints: List[str] = Field(description="Pontos de contato detalhados")
    emotional_state: str = Field(description="Estado emocional do cliente com análise psicológica")
    opportunities: List[str] = Field(description="Oportunidades de conversão com justificativa técnica")

class ClienteMercado(BaseModel):
    tam_sam_som: str = Field(description="Análise quantitativa exaustiva do mercado brasileiro (mín 4 parágrafos)")
    analise_setorial_detalhada: str = Field(description="Análise profunda de tendências e riscos do setor (novo campo para densidade)")
    segmentacao: Segmentacao = Field(description="Matriz de segmentação")
    persona: Persona = Field(description="Perfil ultra-denso da Persona")
    customer_journey: List[CustomerJourneyPhase] = Field(description="Jornada do cliente em 3 fases ultra-detalhadas")

# ============================================================
# MÓDULO 2: PROBLEMA & SOLUÇÃO
# ============================================================

class PropostaValor(BaseModel):
    declaracao: str = Field(description="Declaração de valor impactante")
    problema_central: str = Field(description="O problema 'dor de cabeça' que resolve (análise profunda)")
    solucao_proposta: str = Field(description="A solução e como ela resolve o problema (detalhamento técnico)")
    diferenciais_unicos: List[str] = Field(description="Por que somos melhores que o 'status quo' (justificativa longa)")

class CompetitorMatrixItem(BaseModel):
    name: str = Field(description="Nome do concorrente")
    convenience: float = Field(description="Nota 1-10")
    innovation: float = Field(description="Nota 1-10")
    price: float = Field(description="Nota 1-10")
    quality: float = Field(description="Nota 1-10")
    support: float = Field(description="Nota 1-10")
    technology: float = Field(description="Nota 1-10")
    average_score: float = Field(description="Média")
    justificativa_notas: str = Field(description="Justificativa longa para as notas atribuídas (novo campo para densidade)")

class AnaliseConcorrencia(BaseModel):
    competitor_matrix: List[CompetitorMatrixItem] = Field(description="Matriz comparativa com 2 concorrentes reais + o seu negócio")
    estrategia_defensiva: str = Field(description="Como vamos nos diferenciar e nos proteger (mín 4 parágrafos)")

class ProblemaSolucao(BaseModel):
    proposta_valor: PropostaValor = Field(description="Mapeamento da Proposta de Valor")
    analise_concorrencia: AnaliseConcorrencia = Field(description="Análise da concorrência e diferencial")

# ============================================================
# MÓDULO 3: ESTRATÉGIA (SWOT EXPANDIDA)
# ============================================================

class ItemSWOT(BaseModel):
    descricao: str = Field(description="Fator SWOT")
    impact_level: str = Field(description="Impacto: High ou Low")
    strategic_action: str = Field(description="Ação estratégica concreta e detalhada")

class MatrizSWOTExpandida(BaseModel):
    forcas: List[ItemSWOT]
    fraquezas: List[ItemSWOT]
    oportunidades: List[ItemSWOT]
    ameacas: List[ItemSWOT]

class Estrategia(BaseModel):
    missao: str = Field(description="Missão com justificativa de propósito")
    visao: str = Field(description="Visão de futuro detalhada")
    valores: List[str] = Field(description="Valores com descrição do comportamento esperado")
    pilares_culturais: str = Field(description="Como a cultura suporta a estratégia (análise densa)")
    swot: MatrizSWOTExpandida = Field(description="SWOT com impacto e ações")
    objetivos_smart: List[str] = Field(description="Metas SMART detalhadas (mín 5)")
    analise_de_riscos_detalhada: str = Field(description="Plano de mitigação de riscos estratégicos (novo campo para densidade)")

# ============================================================
# MÓDULO 4: MARKETING & VENDAS (GROWTH)
# ============================================================

class SalesFunnelStage(BaseModel):
    stage_name: str = Field(description="Stage: Top, Middle ou Bottom")
    description: str = Field(description="Descrição exaustiva da etapa AIDA (mín 3 parágrafos)")
    invested_budget: float = Field(description="Orçamento (R$)")
    reached_people: int = Field(description="Alcance")
    call_to_action_people: int = Field(description="Conversões")
    cac: float = Field(description="CAC da etapa")
    conversion_rate: float = Field(description="Taxa (%)")

class SalesFunnel(BaseModel):
    top: SalesFunnelStage
    middle: SalesFunnelStage
    bottom: SalesFunnelStage
    global_cac: float
    ltv: float
    ltv_cac_ratio: float
    justificativa_metrica_growth: str = Field(description="Análise narrativa das métricas de growth (novo campo para densidade)")

class ExperimentHypothesis(BaseModel):
    hypothesis_description: str
    validation_method: str
    success_metric: str
    deadline: int
    status: str

class MarketingPlan(BaseModel):
    sales_funnel: SalesFunnel = Field(description="Funil de vendas detalhado AIDA")
    experiment_board: List[ExperimentHypothesis] = Field(description="Quadro de experimentação")
    canais_aquisicao_detalhados: str = Field(description="Análise profunda de cada canal prioritário (novo campo para densidade)")

# ============================================================
# MÓDULO 5: FINANÇAS (DRE 12 MESES)
# ============================================================

class FinancialInvestment(BaseModel):
    item: str
    value: float
    justificativa_item: str = Field(description="Por que este investimento é necessário? (detalhe longo)")

class FinancialScenario(BaseModel):
    scenario_name: str = Field(description="Optimistic, Pessimistic ou Probable")
    estimated_revenue: float
    estimated_profit: float
    justification: str = Field(description="Justificativa macro e microeconômica longa")

class DREMonth(BaseModel):
    month_name: str
    revenue: float
    taxes: float
    variable_costs: float
    contribution_margin: float
    fixed_costs: float
    net_profit: float

class FinancialPlan(BaseModel):
    fixed_investments: List[FinancialInvestment]
    pre_operational_investments: List[FinancialInvestment]
    working_capital: float
    dre_12_months: List[DREMonth]
    scenarios: List[FinancialScenario]
    viability_indicators: Dict[str, float]
    comentarios_financeiros: str = Field(description="Análise narrativa ultra-densa (mín 5 parágrafos)")
    sustentabilidade_financeira: str = Field(description="Plano de sustentabilidade e reinvestimento (novo campo para densidade)")

# ============================================================
# MÓDULO 6: OPERAÇÕES
# ============================================================

class PlanoOperacional(BaseModel):
    atividades_chaves: List[str]
    parceiros_chaves: List[str]
    infraestrutura: str = Field(description="Detalhamento físico e tecnológico exaustivo")
    aspectos_legais: str = Field(description="Burocracia, licenças e conformitá (detalhe longo)")
    quadro_equipe: List[str] = Field(description="Descrição de cargos e responsabilidades densa")
    fluxograma_operacional: str = Field(description="Descrição narrativa do passo a passo da operação (novo campo para densidade)")

# ============================================================
# MASTER SCHEMA: S7teBusinessPlanV3.1
# ============================================================

class S7teBusinessPlanV3(BaseModel):
    """Schema Master V3.1 - Padrão 74 Páginas SEBRAE High Density."""
    sumario_executivo: str = Field(description="Resumo executivo ultra-denso e persuasivo (mínimo 5 parágrafos)")
    cliente_mercado: ClienteMercado
    problema_solucao: ProblemaSolucao
    estrategia: Estrategia
    marketing: MarketingPlan
    financas: FinancialPlan
    operacional: PlanoOperacional
