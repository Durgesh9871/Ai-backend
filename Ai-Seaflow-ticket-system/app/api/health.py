

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])



@router.get("", summary="Check API health", response_description="API is running")
async def health_check():
    return {"status": "ok health check"}