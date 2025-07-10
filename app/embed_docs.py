import argparse
from app.core.document_loader import load_documents
from app.core.embedder import Embedder
from app.core.vector_store import VectorStore


def main(
    collection_name: str | None,
    delete_old_embedding: bool | None,
    path: str = "data",
):
    chunks = load_documents(path)
    texts = [chunk["text"] for chunk in chunks]

    embedder = Embedder()
    embeddings = embedder.embed(texts)

    vector_store = VectorStore(delete_old_collection=delete_old_embedding)
    vector_store.add_embeddings(chunks, embeddings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed and store legal documents.")

    parser.add_argument(
        "--path",
        type=str,
        default="data",
        help="Path to folder containing legal documents",
    )
    parser.add_argument(
        "--collection_name",
        type=str,
        default=None,
        help="Name of the Chroma collection",
    )
    parser.add_argument(
        "--delete_old_embedding",
        action="store_true",
        help="Delete existing embeddings before adding new ones",
    )

    args = parser.parse_args()
    print(args)
    main(
        path=args.path,
        collection_name=args.collection_name,
        delete_old_embedding=args.delete_old_embedding,
    )
