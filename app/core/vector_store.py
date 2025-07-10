from typing import Any
import numpy as np
from chromadb import PersistentClient
from chromadb.errors import NotFoundError
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "./vector_store",
        collection_name: str = "legal_chunks",
        delete_old_collection: bool = False,
    ):
        try:
            self.client = PersistentClient(path=persist_directory)
            if delete_old_collection:
                try:
                    self.client.delete_collection(name=collection_name)
                    logger.info(f"Deleted collection: {collection_name}")
                except NotFoundError:
                    logger.warning(
                        f"Collection '{collection_name}' does not exist. Nothing to delete."
                    )
                except Exception as e:
                    logger.exception(
                        f"Error deleting collection '{collection_name}': {e}"
                    )
                    raise RuntimeError(
                        "An error occurred while deleting the collection."
                    ) from e

            self.collection = self.client.get_or_create_collection(name=collection_name)

        except Exception as e:
            logger.exception(f"Failed to initialize VectorStore: {e}")
            raise RuntimeError("Vector store initialization failed.") from e

    def add_embeddings(self, chunks: list[dict[str, Any]], embeddings: np.ndarray):
        """
        Store embedded chunks into the Chroma collection.
        """
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=[chunk["text"] for chunk in chunks],
                metadatas=[
                    {"source": chunk["source"], "chunk_id": chunk["chunk_id"]}
                    for chunk in chunks
                ],
                ids=[f"{chunk['source']}_{chunk['chunk_id']}" for chunk in chunks],
            )

        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Failed to prepare or add embeddings: {e}")
            raise RuntimeError("Invalid input format while adding embeddings.") from e

        except Exception as e:
            logger.exception(f"Unexpected error in add_embeddings: {e}")
            raise RuntimeError("An error occurred while storing embeddings.") from e

    def query(self, embedding: np.ndarray, top_k: int = 5) -> list[Dict]:
        try:
            results = self.collection.query(query_embeddings=embedding, n_results=top_k)
            return [
                {"text": doc, "source": meta["source"], "chunk_id": meta["chunk_id"]}
                for doc, meta in zip(results["documents"][0], results["metadatas"][0])
            ]

        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Failed to parse query results: {e}")
            raise RuntimeError(
                "Failed to parse query results from vector store."
            ) from e

        except Exception as e:
            logger.exception(f"Error querying vector store: {e}")
            raise RuntimeError("An error occurred during vector store query.") from e
