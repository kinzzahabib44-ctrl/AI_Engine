import re
import logging

def chunk_documents(docs, chunk_size=500, chunk_overlap=100):
   
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []

    for doc_index, doc in enumerate(docs):
        text = re.sub(r'\s+', ' ', doc.get("page_content", "")).strip()
        if not text:
            logging.warning(f"Document {doc_index} is empty, skipping.")
            continue

        metadata = doc.get("metadata", {})
        text_len = len(text)

        start = 0
        chunk_index = 0

        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index,
                    "chunk_start": start,
                    "chunk_end": end,
                    "source_type": metadata.get("type", "unknown")
                }
            })

            start += chunk_size - chunk_overlap
            chunk_index += 1

    logging.info(f"Created {len(chunks)} chunks from {len(docs)} documents.")
    return chunks
