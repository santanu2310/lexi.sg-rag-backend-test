from fastapi import APIRouter

from app.router.rag.router import router as rag_router

router: APIRouter = APIRouter()

router.include_router(rag_router)
