from fastapi import APIRouter, HTTPException, status
from app.core.rag import RAGPipeline
from app.models.output import RAGResponse
from app.models.input import QueryRequest

router: APIRouter = APIRouter()
rag_pipeline = RAGPipeline()


@router.post(path="/query")
async def query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="`query` field can't be empty",
        )
    output: RAGResponse = rag_pipeline.run(query=request.query, top_k=2)

    return output
