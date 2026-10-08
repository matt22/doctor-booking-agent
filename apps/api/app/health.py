from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live() -> dict[str, str]:
    """Process is running."""
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
    """Ready to serve traffic. Will check the database once PostgreSQL is added."""
    return {"status": "ok"}
