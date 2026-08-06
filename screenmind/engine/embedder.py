"""
Embedding Engine for ScreenMind
Generates semantic embeddings for activity summaries using OpenAI-compatible API.
Uses all-MiniLM-L6-v2 model (384 dimensions) for vector compatibility.
"""

import logging
from typing import List, Optional

import httpx

from screenmind.config import settings

logger = logging.getLogger("screenmind.engine.embedder")

# Timeout for embedding API calls
EMBEDDING_TIMEOUT = 30.0
HEALTH_TIMEOUT = 5.0

# Fixed embedding model - cannot be changed to ensure vector data compatibility
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


class Embedder:
    """
    Generates 384-dimensional embeddings using all-MiniLM-L6-v2 via API.
    Uses OpenAI-compatible embeddings endpoint with separate BASE_URL and API key.
    Model is fixed to all-MiniLM-L6-v2 to ensure vector data compatibility.
    """

    def __init__(self):
        self._model_name = EMBED_MODEL_NAME
        self._initialized = False
        self._available = False
        
    def _check_availability(self) -> bool:
        """Check if embedding API is reachable and healthy."""
        try:
            url = f"{self._base_url()}/models"
            headers = {}
            if settings.embed_api_key:
                headers["Authorization"] = f"Bearer {settings.embed_api_key}"
            response = httpx.get(url, timeout=HEALTH_TIMEOUT, headers=headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def _base_url(self) -> str:
        """Get the base URL for the embedding API endpoint."""
        return settings.embed_api_base_url.rstrip("/")
    
    def _ensure_initialized(self):
        """Check embedding API availability on first use."""
        if not self._initialized:
            logger.info(f"Checking embedding API availability at {self._base_url()}...")
            self._available = self._check_availability()
            self._initialized = True
            if self._available:
                logger.info(f"Embedding API available. Model: {self._model_name}")
            else:
                logger.error("Embedding API unavailable — semantic search will be disabled")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding vector for a text string via API.

        Args:
            text: The text to embed (typically activity summary + details).

        Returns:
            List of 384 floats representing the semantic embedding.
            
        Raises:
            RuntimeError: If embedding API is unavailable.
        """
        self._ensure_initialized()
        if not self._available:
            raise RuntimeError("Embedding API unavailable")
        
        url = f"{self._base_url()}/embeddings"
        payload = {
            "model": self._model_name,
            "input": text,
        }
        
        headers = {"Content-Type": "application/json"}
        if settings.embed_api_key:
            headers["Authorization"] = f"Bearer {settings.embed_api_key}"
        
        try:
            response = httpx.post(url, json=payload, headers=headers, timeout=EMBEDDING_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            embedding = data["data"][0]["embedding"]
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    def embed_texts_batch(self, texts: List[str], batch_size: Optional[int] = None) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in a single batch API call.
        
        Args:
            texts: List of text strings to embed.
            batch_size: Optional batch size override (default from settings.embed_api_batch_size).
            
        Returns:
            List of embedding vectors (each is a list of 384 floats).
            
        Raises:
            RuntimeError: If embedding API is unavailable.
        """
        self._ensure_initialized()
        if not self._available:
            raise RuntimeError("Embedding API unavailable")
        
        if not texts:
            return []
        
        # Use configured batch size or provided override
        effective_batch_size = batch_size if batch_size is not None else settings.embed_api_batch_size
        
        all_embeddings = []
        # Process in batches if text list exceeds batch size
        for i in range(0, len(texts), effective_batch_size):
            batch = texts[i:i + effective_batch_size]
            url = f"{self._base_url()}/embeddings"
            payload = {
                "model": self._model_name,
                "input": batch,
            }
            
            headers = {"Content-Type": "application/json"}
            if settings.embed_api_key:
                headers["Authorization"] = f"Bearer {settings.embed_api_key}"
            
            try:
                response = httpx.post(url, json=payload, headers=headers, timeout=EMBEDDING_TIMEOUT)
                response.raise_for_status()
                data = response.json()
                # Sort by index to maintain order
                embeddings_sorted = sorted(data["data"], key=lambda x: x["index"])
                all_embeddings.extend([item["embedding"] for item in embeddings_sorted])
            except Exception as e:
                logger.error(f"Failed to generate batch embeddings: {e}")
                raise
        
        return all_embeddings
    
    def embed_activity(
        self,
        summary: str = "",
        details: str = "",
        visible_text: Optional[List[str]] = None,
        app_name: str = "",
        category: str = "",
        scene_description: str = "",
    ) -> List[float]:
        """
        Generate an embedding for an activity by combining multiple text fields.
        This produces better search results than embedding just the summary.

        Args:
            summary: Activity summary from LLM.
            details: Detailed context from LLM.
            visible_text: Text snippets visible on screen.
            app_name: Application name.
            category: Activity category.
            scene_description: Rich visual narration of the screenshot.

        Returns:
            384-dimensional embedding vector.
        """
        # Combine fields with decreasing importance
        parts = []
        if summary:
            parts.append(summary)
        if scene_description:
            # Truncate for embedding (MiniLM has 256 token limit)
            parts.append(scene_description[:500])
        if details:
            parts.append(details)
        if app_name:
            parts.append(f"Application: {app_name}")
        if category:
            parts.append(f"Category: {category}")
        if visible_text:
            parts.append("Visible: " + " | ".join(visible_text[:5]))

        combined = ". ".join(parts)
        return self.embed_text(combined)

    def search(
        self,
        query: str,
        embeddings: List[List[float]],
        top_k: int = 10,
    ) -> List[tuple]:
        """
        Find the most similar embeddings to a query using cosine similarity.

        Args:
            query: Natural language search query.
            embeddings: List of stored embedding vectors.
            top_k: Number of top results to return.

        Returns:
            List of (index, similarity_score) tuples, sorted by relevance.
        """
        import numpy as np
        
        self._ensure_initialized()
        if not self._available or not embeddings:
            return []

        query_embedding = np.array(self.embed_text(query))
        stored = np.array(embeddings)

        # Cosine similarity (embeddings are already normalized)
        similarities = stored @ query_embedding

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            (int(idx), float(similarities[idx]))
            for idx in top_indices
            if similarities[idx] > 0.1  # Min relevance threshold
        ]

    @property
    def dimensions(self) -> int:
        """Embedding dimensions (384 for all-MiniLM-L6-v2)."""
        return 384

    @property
    def is_available(self) -> bool:
        """Check if the embedding API can be reached."""
        self._ensure_initialized()
        return self._available
