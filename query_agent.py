import logging

class QueryAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def handle_query(self, query):
        try:
            # Enhanced to support different types of search strategies
            return self.vector_store.search(query, search_type="similarity")
        except Exception as e:
            logging.error(f"Error handling query: {e}")
            return []
