import logging
from datetime import datetime
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

def create_rag_chain(llm, vector_store):
    try:
        now = datetime.now()
        formatted_date = now.strftime("%m/%d/%Y")
        formatted_time = now.strftime("%H:%M:%S")
        
        prompt = ChatPromptTemplate.from_template(
            f"""
            Answer the following question based only on the provided context:
            <context>
            Date: {formatted_date}
            Time: {formatted_time}
            {{context}}
            </context>
            Question: {{input}}
            """
        )

        docs_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector_store.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, docs_chain)
        
        logging.info("RAG chain created successfully.")
        return retrieval_chain
    except Exception as e:
        logging.error(f"Error creating RAG chain: {e}")
        return None
