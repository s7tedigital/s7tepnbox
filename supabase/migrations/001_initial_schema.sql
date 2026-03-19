-- Migration: 001_initial_schema.sql
-- Description: Creates the baseline tables for S7te Plan Builder.

-- 1. users table: Extends Supabase's auth.users
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user'::text,
    stripe_customer_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Trigger to automatically create a public.users row on sign up in auth.users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (new.id, new.email);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 2. workspaces table: Support for multitenant / consultant setups
CREATE TABLE public.workspaces (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. business_plans table: Main entity storing chat state, JSONs and PDF metadata
CREATE TYPE plan_status AS ENUM ('draft', 'generating', 'completed', 'failed');

CREATE TABLE public.business_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'Novo Plano S7te',
    status plan_status DEFAULT 'draft' NOT NULL,
    raw_chat_context JSONB DEFAULT '[]'::jsonb NOT NULL,
    financial_data_jsonb JSONB DEFAULT '{}'::jsonb NOT NULL,
    strategy_data_jsonb JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. invoices table: Tracks payments (Hybrid Model: Pay-per-Plan individual purchases OR SaaS Subscriptions)
CREATE TABLE public.invoices (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    plan_id UUID REFERENCES public.business_plans(id) ON DELETE SET NULL, -- Nullable if it's a general SaaS sub instead of payload
    stripe_invoice_id TEXT UNIQUE NOT NULL,
    amount_paid INTEGER NOT NULL, -- Stored in cents (Stripe standard)
    currency TEXT DEFAULT 'BRL' NOT NULL,
    status TEXT NOT NULL, -- e.g. 'paid', 'open'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Utility: Trigger to automatically update "updated_at" timestamps
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = timezone('utc'::text, now());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER set_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE PROCEDURE set_updated_at();
CREATE OR REPLACE TRIGGER set_workspaces_updated_at BEFORE UPDATE ON public.workspaces FOR EACH ROW EXECUTE PROCEDURE set_updated_at();
CREATE OR REPLACE TRIGGER set_plans_updated_at BEFORE UPDATE ON public.business_plans FOR EACH ROW EXECUTE PROCEDURE set_updated_at();
