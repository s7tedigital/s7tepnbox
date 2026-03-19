from fastapi import APIRouter, Depends, HTTPException, Request, status
import stripe
import os

from core.security import get_current_user_id

router = APIRouter(prefix="/api/v1/stripe", tags=["stripe"])

# Setup Stripe
# Use os.getenv('STRIPE_SECRET_KEY') no ambiente de produção
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_123")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock_123")

@router.post("/create-checkout-session")
async def create_checkout_session(plan_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Cria uma sessão no Stripe Checkout para o usuário comprar o plano gerado.
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'Plano Executivo #{plan_id}',
                            'description': 'Exportação Completa e PDF do S7te Plan Builder',
                        },
                        'unit_amount': 9700, # R$ 97,00 em centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"http://localhost:3000/plan/{plan_id}?success=true",
            cancel_url=f"http://localhost:3000/plan/{plan_id}?canceled=true",
            client_reference_id=user_id,
            metadata={
                "plan_id": plan_id,
                "user_id": user_id
            }
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Recebe os eventos assíncronos do Stripe para atualizar o status do Invoice/Plano.
    Essencial: Usar DB Supabase Client server-side aqui com service_role para by-pass de RLS,
    pois essa rota é chamada pelo Stripe, não pelo Frontend Autenticado.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        # Verifica a assinatura do Webhook para garantir que veio do Stripe
        # Em modo DEV sem chave real a verificação falhará, então ignoramos com mock bypass se a chave for mock
        if endpoint_secret == "whsec_mock_123":
            # Extraindo JSON mock manual sem verificar assinatura
            import json
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
        else:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Extrai os metadados injetados durante a criação
        plan_id = session.metadata.get("plan_id")
        user_id = session.metadata.get("user_id")
        
        print(f"[STRIPE WEBHOOK] Pagamento confirmado! Liberando PDF para Plan ID: {plan_id} (User: {user_id})")
        
        # TODO: Atualizar o Status no DB Supabase
        # supabase.table('invoices').update({'status': 'paid'}).eq('plan_id', plan_id).execute()
        
    return {"status": "success"}
