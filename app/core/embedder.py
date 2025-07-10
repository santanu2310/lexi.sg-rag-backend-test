from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Convert a list of text chunks into embeddings.
        """
        return self.model.encode(
            texts, show_progress_bar=True, convert_to_numpy=True
        ).tolist()
