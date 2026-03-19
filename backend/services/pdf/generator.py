import os
import logging
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

logger = logging.getLogger(__name__)

# Pegando o caminho absoluto para o diretório de templates
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Diretório onde os PDFs gerados são salvos
PDF_OUTPUT_DIR = "/tmp/s7te_pdfs"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

class SafeDict(dict):
    """
    Um dicionário que engole chaves inexistentes e retorna outro SafeDict vazio.
    Ideal para templates Jinja2 rigorosos, permitindo chaining infinito
    (ex: plan.cliente_mercado.persona.nome_ficticio) sem lançar AttributeError
    se um nó pai no JSON estiver faltando.
    """
    def __getattr__(self, name):
        val = self.get(name, SafeDict())
        if isinstance(val, dict) and not isinstance(val, SafeDict):
            return SafeDict(val)
        return val

    def __getitem__(self, key):
        val = super().get(key, SafeDict())
        if isinstance(val, dict) and not isinstance(val, SafeDict):
            return SafeDict(val)
        return val

    def __str__(self):
        if not bool(dict(self)):
            return ""
        return super().__str__()

    def __bool__(self):
        return bool(dict(self))
    
    # Para que os filtros Jinja como | join funcionem em listas vazias
    def __iter__(self):
        return super().__iter__()

def convert_to_safe_dict(d) -> SafeDict:
    """Converte um dict recursivamente para SafeDict."""
    if not isinstance(d, dict):
        return SafeDict()
    safe_d = SafeDict()
    for k, v in d.items():
        if isinstance(v, dict):
            safe_d[k] = convert_to_safe_dict(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, dict):
                    new_list.append(convert_to_safe_dict(item))
                else:
                    new_list.append(item)
            safe_d[k] = new_list
        else:
            safe_d[k] = v
    return safe_d


def generate_plan_pdf(plan_data: dict) -> bytes:
    """
    Gera as bytes de um PDF utilizando HTML e WeasyPrint para o plano de negócios.
    """
    logger.info("=== GERANDO PDF ===")
    logger.info(f"plan_data top keys: {list(plan_data.keys()) if isinstance(plan_data, dict) else 'NOT A DICT'}")
    
    # Log detalhado de cada seção
    for k, v in (plan_data.items() if isinstance(plan_data, dict) else []):
        if isinstance(v, dict):
            logger.info(f"  [{k}]: dict com {len(v)} chaves -> {list(v.keys())[:10]}")
        elif isinstance(v, list):
            logger.info(f"  [{k}]: lista com {len(v)} itens")
        elif isinstance(v, str):
            logger.info(f"  [{k}]: str ({len(v)} chars) -> {v[:100]}...")
        else:
            logger.info(f"  [{k}]: {type(v).__name__} -> {str(v)[:100]}")
    
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('v2_base.html')

    # Converta o RAW Dict em um SafeDict para o Jinja não explodir
    safe_plan_data = convert_to_safe_dict(plan_data)

    context = {
        "plan": safe_plan_data
    }

    rendered_html = template.render(context)
    
    logger.info(f"HTML renderizado com {len(rendered_html)} caracteres")

    pdf_bytes = HTML(string=rendered_html).write_pdf()
    
    logger.info(f"PDF gerado com {len(pdf_bytes)} bytes")
    
    return pdf_bytes


def generate_and_save_pdf(plan_data: dict, thread_id: str) -> str:
    """
    Gera o PDF e salva em disco. Retorna o caminho completo do arquivo.
    """
    pdf_bytes = generate_plan_pdf(plan_data)
    
    # Sanitizar thread_id para nome de arquivo seguro
    safe_id = "".join(c for c in thread_id if c.isalnum() or c in ('-', '_'))[:50]
    filename = f"s7te_plan_{safe_id}.pdf"
    filepath = os.path.join(PDF_OUTPUT_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(pdf_bytes)
    
    logger.info(f"PDF salvo em disco: {filepath} ({len(pdf_bytes)} bytes)")
    
    return filepath
