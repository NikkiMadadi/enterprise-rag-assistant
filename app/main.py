import streamlit as st
from chunker import chunk_text
from pdf_reader import extract_text_from_pdf
from vector_store import search_chunks, store_chunks
from llm import generate_answer

st.set_page_config(page_title="DataDoc AI", layout="wide")

st.title("DataDoc AI")
st.subheader("Enterprise RAG Assistant")

uploaded_files = st.file_uploader("Upload a PDF document", type=["pdf"], accept_multiple_files=True)

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

if uploaded_files:
    file_names = [file.name for file in uploaded_files]
    if st.session_state.processed_file != file_names:
        with st.spinner("Processing PDF and creating embeddings..."):
            all_chunk_records = []
            for uploaded_file in uploaded_files:
                text = extract_text_from_pdf(uploaded_file)
                chunks = chunk_text(text)

                for chunk in chunks:
                    all_chunk_records.append({
                        "chunk": chunk,
                        "file_name": uploaded_file.name
                    })

            store_chunks(all_chunk_records)

            st.session_state.processed_file = uploaded_file.name
            st.session_state.chunks_count = len(chunks)
            st.session_state.all_chunk_records = all_chunk_records

        st.success(f"PDF processed successfully. Total chunks stored: {len(chunks)}")
    else:
        st.info(f"PDF  processed")

question = st.text_input(
    "Ask a question about the document",
    key="question_input"
)

if question:
    question_lower = question.lower().strip()

    summary_keywords = [
        "all documents",
        "all docs",
        "all pdfs",
        "summarize all",
        "summary of all",
        "what are these documents about",
        "what do these documents say",
        "what does all documents say",
        "what do all documents say"
    ]

    is_summary_question = any(keyword in question_lower for keyword in summary_keywords)

    if is_summary_question:
        all_records = st.session_state.get("all_chunk_records", [])

        # Take first few chunks from each document
        docs_map = {}

        for record in all_records:
            file_name = record["file_name"]

            if file_name not in docs_map:
                docs_map[file_name] = []

            if len(docs_map[file_name]) < 3:
                docs_map[file_name].append(record["chunk"])

        relevant_chunks = []

        for file_name, chunks in docs_map.items():
            combined_text = f"Document: {file_name}\n" + "\n\n".join(chunks)
            relevant_chunks.append(combined_text)

        relevant_metadata = [
            {"file_name": file_name}
            for file_name in docs_map.keys()
        ]

    else:
        with st.spinner("Searching relevant chunks..."):
            results = search_chunks(question, top_k=8)

        relevant_chunks = results["documents"][0]
        relevant_metadata = results["metadatas"][0]

    with st.spinner("Generating answer..."):
        answer = generate_answer(question, relevant_chunks)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Sources used"):
        for i, (document, metadata) in enumerate(
            zip(relevant_chunks, relevant_metadata),
            start=1
        ):
            st.markdown(f"### Source {i}")
            st.write(f"**File:** {metadata['file_name']}")
            st.write(document[:1500])