# Infrastructure, Deployment & Ops — S7te Plan Builder

Guia para gerenciamento do ambiente de produção (VPS, Vercel e Supabase).

## 1. Localização da Infraestrutura

| Componente | Plataforma | Endereço / ID |
|---|---|---|
| **Backend API** | VPS Hostinger (Ubuntu) | `31.97.250.125` (`s7pnbox.s7te.digital`) |
| **Frontend UI** | Vercel | `s7te-plan-builder.vercel.app` |
| **Banco de Dados** | Supabase | Managed Instance |
| **Auth** | Supabase Auth + Iron Session | Shared via Cookies/Middleware |

---

## 2. Backend (VPS Ubuntu)

O backend roda em um ambiente Python isolado controlado pelo `systemd`.

### Comandos de Gestão
- **Status do serviço:** `systemctl status s7pnbox-backend`
- **Reiniciar (após deploy):** `systemctl restart s7pnbox-backend`
- **Logs em tempo real:** `journalctl -u s7pnbox-backend -f`

### Estrutura de Diretórios
- `/var/www/s7pnbox/backend`: Código fonte Python.
- `/var/www/s7pnbox/backend/venv`: Ambiente virtual.
- `/var/www/s7pnbox/backend/.env`: Configurações sensíveis (Gemini, Supabase, Stripe).

### Configuração Nginx
O arquivo em `/etc/nginx/sites-available/s7pnbox.s7te.digital` atua como reverse proxy para a porta `8000`, com suporte a SSE (`proxy_buffering off`) e SSL (Certbot).

---

## 3. Frontend (Vercel)

O deploy é automatizado via Git ou Vercel CLI.

### Variáveis de Ambiente Críticas
- `BACKEND_URL`: `https://s7pnbox.s7te.digital` (URL da VPS)
- `SESSION_SECRET`: String de 32+ chars para encriptação da sessão.
- `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Credenciais do banco.

---

## 4. Pipeline de Deploy (Recomendado)

Atualmente o deploy do backend é feito via `rsync`. Para a equipe de manutenção, recomenda-se:

1.  **Frontend:** Pull Request em `main` disparando deploy automático na Vercel.
2.  **Backend:**
    ```bash
    # Exemplo de script de deploy local para VPS
    rsync -avz --exclude 'venv' --exclude '__pycache__' ./backend/ root@31.97.250.125:/var/www/s7pnbox/backend/
    ssh root@31.97.250.125 "systemctl restart s7pnbox-backend"
    ```

---

## 5. Dependências Nativas (Importante)
O gerador de PDF (WeasyPrint) exige bibliotecas C no Ubuntu. Se recriar o servidor, instale:
```bash
apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libcairo2 fonts-liberation
```
