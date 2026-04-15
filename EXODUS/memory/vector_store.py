import os
import chromadb
from chromadb.config import Settings
from datetime import datetime
import io
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class VectorMemory:
    """
    Long-term Semantic Memory (The Library).
    Stores: Books read, conversations, abstract concepts, patterns.
    """
    
    def __init__(self, persist_dir="chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Collection for general conversation history & facts
        self.context_collection = self.client.get_or_create_collection(
            name="exodus_context",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Collection for behavioral patterns
        self.pattern_collection = self.client.get_or_create_collection(
            name="exodus_patterns",
            metadata={"hnsw:space": "cosine"}
        )

    def save_memory(self, text: str, metadata: dict, category="context"):
        """Saves a text snippet to the vector store."""
        collection = self.pattern_collection if category == "pattern" else self.context_collection
        
        # Add timestamp if missing
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.now().isoformat()

        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[f"{category}_{datetime.now().timestamp()}"]
        )

    def recall(self, query: str, category="context", n_results=3) -> list:
        """Retrieves relevant memories based on semantic similarity."""
        collection = self.pattern_collection if category == "pattern" else self.context_collection
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Flatten results
        return results["documents"][0] if results["documents"] else []

    def count_memories(self):
        return self.context_collection.count()

    def ingest_document(self, text: str, filename: str):
        """Chunks a large document and stores it in vector memory."""
        chunk_size = 1000
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_len = 0
        
        for line in lines:
            if current_len + len(line) > chunk_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_len = 0
            current_chunk.append(line)
            current_len += len(line)
            
        if current_chunk:
            chunks.append("\n".join(current_chunk))
            
        for i, chunk in enumerate(chunks):
            self.save_memory(
                text=chunk,
                metadata={"source": filename, "chunk": i, "type": "document"},
                category="context"
            )
        return len(chunks)

    def ingest_pdf_bytes(self, pdf_bytes: bytes, filename: str):
        """Reads a PDF from bytes and ingests its text."""
        if PdfReader is None:
            raise ValueError("pypdf is not installed")
        
        reader = PdfReader(io.BytesIO(pdf_bytes))
        full_text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"
        
        return self.ingest_document(full_text, filename)
