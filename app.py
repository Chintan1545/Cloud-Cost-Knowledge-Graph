import streamlit as st
from rag import generate_response


# Page Configuration

st.set_page_config(
    page_title="Cloud Cost Knowledge Graph RAG",
    page_icon="☁️",
    layout="wide"
)


# Title Section

st.title("☁️ Cloud Cost Knowledge Graph RAG")
st.markdown("""
Ask intelligent cloud cost questions powered by:

- Neo4j Knowledge Graph  
- Vector Embeddings  
- Groq LLM  
- Hybrid RAG Retrieval  
""")

st.divider()


# Query Input

query = st.text_input(
    "Ask a cloud cost question:",
    placeholder="Example: Which service costs most?"
)


# Run Query

if st.button("Search"):

    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running hybrid retrieval and generating answer..."):
            try:
                answer, context = generate_response(query)

                # Layout Columns
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("📌 Answer")
                    st.success(answer)

                with col2:
                    st.subheader("🔎 Retrieved Context")
                    st.text(context)

            except Exception as e:
                st.error(f"Error: {e}")


# Example Questions

st.divider()

st.subheader("💡 Example Questions")

examples = [
    "Which service costs most?",
    "Show top expensive services",
    "Compare AWS and Azure costs",
    "What is the cost in Production environment?",
    "Which Azure resource is most expensive?"
]

for ex in examples:
    if st.button(ex):
        st.session_state["auto_query"] = ex