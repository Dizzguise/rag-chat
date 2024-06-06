import logging
import yaml
from tkinter import Tk
from langchain_community.llms import Ollama
from document_loader import load_documents
from retrieval_chain import create_rag_chain
from decision_agent import DecisionAgent
from query_agent import QueryAgent
from context_agent import ContextAgent
from web_search import WebSearch

def load_config():
    with open("config.yaml", 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()

    logging.basicConfig(level=getattr(logging, config['logging']['level']))
    root = Tk()
    root.withdraw()  # Hide the root window

    vector_store = load_documents(config)

    llm = Ollama(model=config['llm']['model'])
    web_search = WebSearch(api_key=config['web_search']['api_key'], count=config['web_search']['count'], extra_snippets=config['web_search']['extra_snippets'])
    retrieval_chain = create_rag_chain(llm, vector_store) if vector_store else None
    decision_agent = DecisionAgent(llm)
    query_agent = QueryAgent(vector_store) if vector_store else None
    context_agent = ContextAgent(llm, token_limit=config['llm']['token_limit'])

    def chat(query):
        try:
            if vector_store:
                action_docs = query_agent.handle_query(query)
                managed_context = context_agent.manage_context(query, action_docs)
                decision = decision_agent.decide_action_with_context(query, managed_context)
            else:
                decision = decision_agent.decide_action(query)
            
            if decision == "web":
                optimized_query = decision_agent.optimize_query(query)
                web_results = web_search.search(optimized_query)
                if web_results:
                    managed_context = context_agent.manage_context(query, web_results)
                    response = llm.generate([f"The context is: {managed_context}. The question is: {query}"])
                    print(response.generations[0][0].text.strip())
                else:
                    logging.error("No web results found")
                    print("Sorry, I couldn't find any relevant information.")
            else:
                if vector_store:
                    response = retrieval_chain.invoke({"input": query, "context": managed_context})
                    print(response["answer"])
                else:
                    direct_response = llm.generate([query])
                    print(direct_response.generations[0][0].text.strip())
        except Exception as e:
            logging.error(f"Error in chat function: {e}")

    print("Welcome to the LangChain-based Chatbot. Type 'exit' to quit.")
    while True:
        try:
            user_query = input("You: ")
            if user_query.lower() in ["exit", "quit"]:
                break
            chat(user_query)
        except KeyboardInterrupt:
            print("\nExiting chatbot. Goodbye!")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")

if __name__ == "__main__":
    main()
