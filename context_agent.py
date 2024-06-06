import logging

class ContextAgent:
    def __init__(self, llm, token_limit):
        self.llm = llm
        self.token_limit = token_limit

    def manage_context(self, query, relevant_docs):
        try:
            context = " ".join(relevant_docs)
            if len(context) > self.token_limit:
                # Implement more sophisticated context reduction
                context = context[:self.token_limit]
            return context
        except Exception as e:
            logging.error(f"Error managing context: {e}")
            return ""
