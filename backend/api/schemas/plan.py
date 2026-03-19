from pydantic import BaseModel, Field
from typing import List, Optional

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

class Persona(BaseModel):
    nome_ficticio: str = Field(description="Nome fictício da persona (ex: 'João Motorista')")
    idade: int = Field(description="Idade estimada da persona")
    genero: str = Field(description="Gênero da persona")
    renda_mensal: str = Field(description="Faixa de renda mensal")
    profissao: str = Field(description="Profissão da persona")
    localizacao: str = Field(description="Cidade/Estado de moradia")
    dores_principais: List[str] = Field(description="Lista de dores/problemas que a persona enfrenta")
    desejos: List[str] = Field(description="Lista de desejos e aspirações")
    fluencia_digital: str = Field(description="Nível de fluência digital (Baixa/Média/Alta)")
    canais_preferidos: List[str] = Field(description="Canais de comunicação preferidos (WhatsApp, Instagram, etc.)")
    rotina_manha: str = Field(description="Descrição da rotina matinal típica")
    rotina_tarde: str = Field(description="Descrição da rotina vespertina típica")
    rotina_noite: str = Field(description="Descrição da rotina noturna típica")
    frase_marcante: str = Field(description="Uma frase que a persona diria sobre o problema")

class EtapaJornada(BaseModel):
    descricao: str = Field(description="O que o cliente faz/sente nesta etapa")
    pontos_de_contato: List[str] = Field(description="Onde ele interage com a marca")
    emocoes: str = Field(description="Emoções predominantes nesta etapa")
    oportunidades: List[str] = Field(description="Oportunidades de melhoria identificadas")

class JornadaCliente(BaseModel):
    antes: EtapaJornada = Field(description="Etapa ANTES de conhecer a solução")
    durante: EtapaJornada = Field(description="Etapa DURANTE o uso da solução")
    depois: EtapaJornada = Field(description="Etapa DEPOIS de usar a solução")

class ClienteMercado(BaseModel):
    tam_sam_som: str = Field(description="Análise detalhada do TAM (Total Addressable Market), SAM (Serviceable Available Market) e SOM (Serviceable Obtainable Market)")
    segmentacao: Segmentacao = Field(description="Análise de segmentação com notas")
    persona: Persona = Field(description="Perfil detalhado da persona principal")
    jornada: JornadaCliente = Field(description="Mapeamento da jornada do cliente")

# ============================================================
# MÓDULO 2: PROBLEMA & SOLUÇÃO
# ============================================================

class BeneficiosProposta(BaseModel):
    funcionais: List[str] = Field(description="Benefícios funcionais/práticos do produto")
    emocionais: List[str] = Field(description="Benefícios emocionais (segurança, confiança, etc.)")
    sociais: List[str] = Field(description="Benefícios sociais (status, pertencimento, etc.)")

class PropostaValor(BaseModel):
    declaracao: str = Field(description="Declaração da Proposta de Valor em 1-2 frases impactantes")
    problema_central: str = Field(description="O problema central que resolve")
    solucao_proposta: str = Field(description="A solução proposta sintetizada")
    beneficios: BeneficiosProposta = Field(description="Categorização dos benefícios")
    diferenciais_unicos: List[str] = Field(description="Diferenciais únicos vs. concorrência")

class NotaConcorrente(BaseModel):
    nome: str = Field(description="Nome do concorrente")
    preco: float = Field(description="Nota (0-10): Competitividade de preço")
    qualidade: float = Field(description="Nota (0-10): Qualidade do produto/serviço")
    atendimento: float = Field(description="Nota (0-10): Qualidade do atendimento")
    tecnologia: float = Field(description="Nota (0-10): Nível tecnológico")
    marca: float = Field(description="Nota (0-10): Força da marca")
    nota_media: float = Field(description="Média das notas")

class AnaliseConcorrencia(BaseModel):
    nosso_negocio: NotaConcorrente = Field(description="Notas do nosso negócio")
    concorrente_1: NotaConcorrente = Field(description="Notas do concorrente direto 1")
    concorrente_2: NotaConcorrente = Field(description="Notas do concorrente direto 2")
    conclusao: str = Field(description="Conclusão comparativa: onde ganhamos e onde perdemos")

class ProblemaSolucao(BaseModel):
    proposta_valor: PropostaValor = Field(description="A proposta de valor estruturada")
    analise_concorrencia: AnaliseConcorrencia = Field(description="Tabela comparativa com concorrentes")

# ============================================================
# MÓDULO 3: ESTRATÉGIA (SWOT EXPANDIDA)
# ============================================================

class ItemSWOT(BaseModel):
    descricao: str = Field(description="Descrição do fator")
    impacto: str = Field(description="Impacto: 'alto' ou 'baixo'")
    acao_estrategica: str = Field(description="Ação estratégica recomendada para lidar com este fator")

class MatrizSWOTExpandida(BaseModel):
    forcas: List[ItemSWOT] = Field(description="Forças internas do negócio com impacto e ação")
    fraquezas: List[ItemSWOT] = Field(description="Fraquezas internas com impacto e ação")
    oportunidades: List[ItemSWOT] = Field(description="Oportunidades externas com impacto e ação")
    ameacas: List[ItemSWOT] = Field(description="Ameaças externas com impacto e ação")

class Estrategia(BaseModel):
    visao: str = Field(description="Visão de longo prazo do negócio (3-5 anos)")
    missao: str = Field(description="Missão do negócio")
    valores: List[str] = Field(description="Valores fundamentais da empresa")
    swot: MatrizSWOTExpandida = Field(description="Matriz SWOT detalhada com ações estratégicas")
    objetivos_smart: List[str] = Field(description="Até 5 objetivos SMART para os primeiros 12 meses")

# ============================================================
# MÓDULO 4: FINANÇAS (PNBOX COMPLETO)
# ============================================================

class ItemInvestimento(BaseModel):
    descricao: str = Field(description="Nome do item de investimento")
    valor: float = Field(description="Valor em Reais")

class InvestimentoFixo(BaseModel):
    itens: List[ItemInvestimento] = Field(description="Lista de investimentos fixos (equipamentos, software, etc.)")
    total: float = Field(description="Total do investimento fixo")

class CapitalGiro(BaseModel):
    estoque_inicial: float = Field(description="Valor do estoque inicial (se aplicável)")
    caixa_minimo: float = Field(description="Caixa mínimo necessário para operar nos primeiros meses")
    total: float = Field(description="Total do capital de giro necessário")

class ItemCusto(BaseModel):
    descricao: str = Field(description="Nome do custo")
    valor_mensal: float = Field(description="Valor mensal em Reais")

class CustosFixos(BaseModel):
    itens: List[ItemCusto] = Field(description="Lista de custos fixos mensais (aluguel, salários, cloud, etc.)")
    total_mensal: float = Field(description="Total de custos fixos mensais")

class CustosVariaveis(BaseModel):
    itens: List[ItemCusto] = Field(description="Lista de custos variáveis (comissões, taxas, etc.)")
    percentual_sobre_receita: float = Field(description="Percentual médio dos custos variáveis sobre a receita")
    total_estimado_mensal: float = Field(description="Total estimado de custos variáveis mensais no cenário base")

class MesDRE(BaseModel):
    mes: int = Field(description="Mês (1 a 12)")
    receita_bruta: float = Field(description="Receita bruta projetada")
    deducoes: float = Field(description="Deduções (impostos sobre receita)")
    receita_liquida: float = Field(description="Receita líquida")
    custos_variaveis: float = Field(description="Custos variáveis do mês")
    margem_contribuicao: float = Field(description="Margem de contribuição")
    custos_fixos: float = Field(description="Custos fixos do mês")
    lucro_operacional: float = Field(description="Lucro/Prejuízo operacional")

class DRE_Anual(BaseModel):
    projecao_mensal: List[MesDRE] = Field(description="Projeção mês a mês dos primeiros 12 meses")
    receita_anual_total: float = Field(description="Receita bruta anual total")
    lucro_anual_total: float = Field(description="Lucro/Prejuízo operacional anual total")

class Indicadores(BaseModel):
    lucratividade_percentual: float = Field(description="Lucratividade (%) = Lucro Líquido / Receita Total * 100")
    rentabilidade_percentual: float = Field(description="Rentabilidade (%) = Lucro Líquido / Investimento Total * 100")
    payback_meses: float = Field(description="Prazo de retorno do investimento em meses")
    ponto_equilibrio_faturamento: float = Field(description="Faturamento mensal mínimo para cobrir custos (R$)")
    ponto_equilibrio_unidades: float = Field(description="Quantidade de unidades/assinaturas para atingir equilíbrio")
    roi_anual: float = Field(description="ROI anual estimado (%)")

class Financas(BaseModel):
    investimento_total: float = Field(description="Soma: Investimento Fixo + Capital de Giro")
    investimento_fixo: InvestimentoFixo = Field(description="Detalhamento do investimento fixo")
    capital_giro: CapitalGiro = Field(description="Detalhamento do capital de giro")
    custos_fixos: CustosFixos = Field(description="Detalhamento de custos fixos mensais")
    custos_variaveis: CustosVariaveis = Field(description="Detalhamento de custos variáveis")
    dre_anual: DRE_Anual = Field(description="DRE projetada para 12 meses")
    indicadores: Indicadores = Field(description="Indicadores de viabilidade")

# ============================================================
# MÓDULO 5: FERRAMENTAS COMPLEMENTARES (MARKETING & GROWTH)
# ============================================================

class CanalAquisicao(BaseModel):
    nome: str = Field(description="Nome do canal (ex: Meta Ads, SEO, Outbound)")
    nota_atratividade: float = Field(description="Nota (0-10): Quão atrativo é este canal")
    nota_alcance: float = Field(description="Nota (0-10): Potencial de alcance")
    custo_estimado_mensal: float = Field(description="Investimento mensal estimado neste canal (R$)")
    estrategia: str = Field(description="Breve estratégia de uso do canal")

class EtapaFunil(BaseModel):
    nome: str = Field(description="Nome da etapa (Topo, Meio, Fundo)")
    descricao: str = Field(description="Descrição do que acontece nesta etapa")
    taxa_conversao_estimada: float = Field(description="Taxa de conversão estimada (%)")
    acoes: List[str] = Field(description="Ações específicas para esta etapa")
    metricas_chave: List[str] = Field(description="KPIs para monitorar esta etapa")

class FunilVendas(BaseModel):
    topo: EtapaFunil = Field(description="Topo do funil (Awareness)")
    meio: EtapaFunil = Field(description="Meio do funil (Consideração)")
    fundo: EtapaFunil = Field(description="Fundo do funil (Conversão)")
    cac_projetado: float = Field(description="Custo de Aquisição de Cliente projetado (R$)")
    ltv_projetado: float = Field(description="Lifetime Value projetado (R$)")
    razao_ltv_cac: float = Field(description="Razão LTV/CAC (ideal > 3)")

class HipoteseExperimentacao(BaseModel):
    hipotese: str = Field(description="Hipótese a ser validada")
    metodo_validacao: str = Field(description="Como será validada (entrevista, MVP, teste A/B, etc.)")
    metrica_sucesso: str = Field(description="Métrica que define sucesso")
    prazo_dias: int = Field(description="Prazo para validação em dias")
    status: str = Field(description="Status: 'pendente', 'em_validacao' ou 'validada'")

class QuadroExperimentacao(BaseModel):
    hipoteses: List[HipoteseExperimentacao] = Field(description="Lista de hipóteses de negócio a validar")

class FerramentasComplementares(BaseModel):
    canais_aquisicao: List[CanalAquisicao] = Field(description="Análise dos canais de aquisição com notas")
    funil_vendas: FunilVendas = Field(description="Funil de vendas completo com métricas")
    quadro_experimentacao: QuadroExperimentacao = Field(description="Quadro de experimentação com hipóteses")

# ============================================================
# MÓDULO 6: OPERAÇÕES
# ============================================================

class PlanoOperacional(BaseModel):
    atividades_chaves: List[str] = Field(description="Atividades-chave diárias do negócio")
    parceiros_chaves: List[str] = Field(description="Parceiros e fornecedores essenciais")
    infraestrutura: str = Field(description="Necessidades de infraestrutura (física e tecnológica)")
    aspectos_legais: str = Field(description="Licenças, alvarás e regulamentações necessárias")
    quadro_equipe: List[str] = Field(description="Posições necessárias na equipe inicial")

# ============================================================
# MASTER SCHEMA: S7teBusinessPlanV2
# ============================================================

class S7teBusinessPlanV2(BaseModel):
    """Schema mestre que unifica todos os 6 módulos do Plano de Negócios S7te Digital (Padrão PNBOX)."""
    sumario_executivo: str = Field(description="Resumo executivo denso e completo (mínimo 3 parágrafos)")
    cliente_mercado: ClienteMercado = Field(description="Módulo 1: Análise de Cliente e Mercado")
    problema_solucao: ProblemaSolucao = Field(description="Módulo 2: Problema, Solução e Concorrência")
    estrategia: Estrategia = Field(description="Módulo 3: Estratégia (SWOT, Visão, Missão)")
    financas: Financas = Field(description="Módulo 4: Finanças (Investimento, DRE, Indicadores)")
    ferramentas: FerramentasComplementares = Field(description="Módulo 5: Ferramentas de Marketing e Growth")
    operacional: PlanoOperacional = Field(description="Módulo 6: Plano Operacional")
