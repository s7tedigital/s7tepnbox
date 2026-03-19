-- Migration: 002_rls_policies.sql
-- Description: Applies incredibly strict Row Level Security (RLS) rules adhering to s7te-security-rules.md manifesto.

-- 1. Enable RLS indiscriminately on all core tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.business_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;

-- 2. Users Table Policies
-- Users can only READ and UPDATE their own raw user data.
-- Deletion or Creation MUST happen via backend `service_role` or trigger.
CREATE POLICY "Strict isolated read for own user profile"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Strict isolated update for own user profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id);

-- 3. Workspaces Table Policies
-- Only owners can view or manipulate their workspaces.
CREATE POLICY "Owner isolation for select workspaces"
    ON public.workspaces FOR SELECT
    USING (auth.uid() = owner_id);

CREATE POLICY "Owner rule for insert workspaces"
    ON public.workspaces FOR INSERT
    WITH CHECK (auth.uid() = owner_id);

CREATE POLICY "Owner rule for update workspaces"
    ON public.workspaces FOR UPDATE
    USING (auth.uid() = owner_id);

CREATE POLICY "Owner rule for delete workspaces"
    ON public.workspaces FOR DELETE
    USING (auth.uid() = owner_id);

-- 4. Business Plans Table Policies
-- The soul of the startup. Can only be retrieved and manipulated by the authenticated creator.
CREATE POLICY "Strict isolated select for own business plans"
    ON public.business_plans FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Locked insert for own business plans"
    ON public.business_plans FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Locked update for own business plans"
    ON public.business_plans FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Locked delete for own business plans"
    ON public.business_plans FOR DELETE
    USING (auth.uid() = user_id);

-- 5. Invoices / Payments Policies
-- Billing transparency but strictly read-only for the client.
-- Invoices are created directly by Stripe Webhook triggers processing via `service_role` Python backend.
CREATE POLICY "Read-only isolation for own invoices"
    ON public.invoices FOR SELECT
    USING (auth.uid() = user_id);

-- We intentionally DO NOT create INSERT, UPDATE, or DELETE policies on invoices 
-- because frontend clients must never write to billing data.
