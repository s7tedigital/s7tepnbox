from fastapi import Header, HTTPException, status

async def get_current_user_id(x_user_id: str = Header(default=None, alias="X-User-Id")) -> str:
    """
    Dependency to extract and validate the X-User-Id header injected by the Next.js API Proxy.
    If the header is missing, the request is definitively unauthenticated.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authentication Header. Must pass through S7te Proxy.",
        )
    return x_user_id
