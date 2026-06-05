import re


def clean_text(text):
    text = re.sub(r"©\d{4}.*?rights reserved", "", text, flags=re.IGNORECASE)
    text = re.sub(r"--- Page \d+ ---", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=1200, overlap=200):
    text = clean_text(text)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks