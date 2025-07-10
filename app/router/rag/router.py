from fastapi import APIRouter, Query, HTTPException, status
from app.core.rag import RAGPipeline
from app.models.output import RAGResponse

router: APIRouter = APIRouter()
rag_pipeline = RAGPipeline()


@router.get(path="/query")
async def query(q: str | None = Query(None, description="Query RAG")):
    if not q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="query parameter can't be empty",
        )
    output: RAGResponse = rag_pipeline.run(query=q, top_k=2)

    return output
