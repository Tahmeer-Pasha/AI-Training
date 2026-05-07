"""
Vector Store Implementation for Resume Shortlisting

This module provides a simple vector store implementation for semantic similarity
calculations. It uses basic TF-IDF concepts and cosine similarity for document
matching without requiring external vector databases.

Author: [Your Name]
Date: 2024
"""

from __future__ import annotations
from collections import Counter
from typing import Any, List, Dict, Optional
import math
import re


def normalize_text(text: str) -> List[str]:
    """
    Normalize text by extracting alphanumeric tokens in lowercase.
    
    Args:
        text: Input text to normalize
        
    Returns:
        List of normalized tokens
    """
    return re.findall(r"\w+", text.lower())


def cosine_similarity(vec_a: Counter[str], vec_b: Counter[str]) -> float:
    """
    Calculate cosine similarity between two term frequency vectors.
    
    Args:
        vec_a: First vector (Counter of terms)
        vec_b: Second vector (Counter of terms)
        
    Returns:
        Cosine similarity score between 0.0 and 1.0
    """
    # Calculate dot product
    dot_product = sum(vec_a[token] * vec_b[token] for token in vec_a if token in vec_b)
    
    # Calculate norms
    norm_a = math.sqrt(sum(value * value for value in vec_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vec_b.values()))
    
    # Avoid division by zero
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


class VectorStore:
    """
    Simple vector store for document similarity calculations.
    
    This implementation uses TF-IDF concepts and cosine similarity to find
    semantically similar documents. It's designed to be lightweight and
    doesn't require external dependencies like ChromaDB.
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the vector store.
        
        Args:
            model_name: Not used in this implementation, kept for compatibility
        """
        self.documents: List[Dict[str, Any]] = []
        self.model_name = model_name or "simple_tfidf"
    
    def clear(self) -> None:
        """Clear all stored documents."""
        self.documents = []
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]]) -> None:
        """
        Add multiple documents to the vector store.
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dictionaries for each document
        """
        for i, text in enumerate(documents):
            metadata = metadatas[i] if i < len(metadatas) else {}
            self.add_document(text, f"doc_{len(self.documents)}", metadata)
    
    def add_document(self, text: str, source: str, metadata: Dict[str, Any]) -> None:
        """
        Add a single document to the vector store.
        
        Args:
            text: Document text content
            source: Document identifier/source
            metadata: Additional metadata for the document
        """
        # Create term frequency vector
        vector = Counter(normalize_text(text))
        
        self.documents.append({
            "text": text,
            "source": source,
            "metadata": metadata,
            "vector": vector
        })
    
    def query(self, query_text: str, n_results: int = 3, 
              filter_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: Query text to search for
            n_results: Maximum number of results to return
            filter_type: Optional filter for document type
            
        Returns:
            Dictionary with query results including documents, distances, and metadatas
        """
        if not self.documents:
            return {
                "documents": [[]],
                "distances": [[]],
                "metadatas": [[]]
            }
        
        query_vector = Counter(normalize_text(query_text))
        candidates = []
        
        for doc in self.documents:
            # Apply filter if specified
            if filter_type and doc["metadata"].get("type") != filter_type:
                continue
            
            # Calculate similarity score
            score = cosine_similarity(query_vector, doc["vector"])
            
            candidates.append({
                "text": doc["text"],
                "source": doc["source"],
                "metadata": doc["metadata"],
                "score": float(score),
                "distance": 1.0 - float(score)  # Convert similarity to distance
            })
        
        # Sort by similarity (highest first)
        candidates.sort(key=lambda item: item["score"], reverse=True)
        
        # Limit results
        top_candidates = candidates[:n_results]
        
        # Format results to match ChromaDB interface
        return {
            "documents": [[candidate["text"] for candidate in top_candidates]],
            "distances": [[candidate["distance"] for candidate in top_candidates]],
            "metadatas": [[candidate["metadata"] for candidate in top_candidates]]
        }
    
    def search(self, query: str, top_k: int = 3, 
               filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Legacy search method for backward compatibility.
        
        Args:
            query: Query text
            top_k: Number of results to return
            filter_type: Optional document type filter
            
        Returns:
            List of search results with text, source, and score
        """
        if not self.documents:
            return []
        
        query_vector = Counter(normalize_text(query))
        candidates = []
        
        for doc in self.documents:
            if filter_type and doc["metadata"].get("type") != filter_type:
                continue
            
            score = cosine_similarity(query_vector, doc["vector"])
            candidates.append({
                "text": doc["text"],
                "source": doc["source"],
                "score": float(score)
            })
        
        candidates.sort(key=lambda item: item["score"], reverse=True)
        return candidates[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with store statistics
        """
        return {
            "total_documents": len(self.documents),
            "model_name": self.model_name,
            "avg_doc_length": sum(len(doc["text"]) for doc in self.documents) / max(1, len(self.documents))
        }


# Alias for backward compatibility
SimpleVectorStore = VectorStore