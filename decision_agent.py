import logging
from datetime import datetime

class DecisionAgent:
    def __init__(self, llm):
        self.llm = llm

    def decide_action(self, query):
        now = datetime.now()
        formatted_date = now.strftime("%m/%d/%Y")
        formatted_time = now.strftime("%H:%M:%S")
        
        decision_prompt = f"""
        You are part of a decision chain. You must respond with ONLY the word 'direct' or 'web' and nothing else. If you can answer the question based on internal data or provided context, you must say 'direct' and nothing else. If you require a web search for an accurate answer, you must respond with 'web' and nothing else. DO NOT explain your decision.
        Today is: {formatted_date}
        The time is: {formatted_time}
        Question: {query}
        
        Your response must only be 'direct' or 'web' and nothing else. The word you choose decides if we perform a web search or not. DO NOT explain your decision.
        """
        try:
            decision_response = self.llm.generate([decision_prompt])
            action = decision_response.generations[0][0].text.strip().lower()
            logging.info(f"Decision: {action}")
            return action
        except Exception as e:
            logging.error(f"Error in decision-making process: {e}")
            return "direct"  # Fallback action

    def decide_action_with_context(self, query, context):
        now = datetime.now()
        formatted_date = now.strftime("%m/%d/%Y")
        formatted_time = now.strftime("%H:%M:%S")

        decision_prompt = f"""
        You are part of a decision chain. You must respond with ONLY the word 'direct' or 'web' and nothing else. If you can answer the question based on internal data or provided context, you must say 'direct' and nothing else. If you require a web search for an accurate answer, you must respond with 'web' and nothing else. DO NOT explain your decision.
        Date: {formatted_date}
        Time: {formatted_time}
        Context: {context}
        Questions: {query}
        
        Saying 'web' gives you access to real time data when necessary.
        Your response must only be 'direct' or 'web' and nothing else. The word you choose decides if we perform a web search or not. DO NOT explain your decision.
        """
        try:
            decision_response = self.llm.generate([decision_prompt])
            action = decision_response.generations[0][0].text.strip().lower()
            logging.info(f"Decision: {action}")
            return action
        except Exception as e:
            logging.error(f"Error in decision-making process: {e}")
            return "web"  # Fallback action if context is insufficient

    def optimize_query(self, query):
        now = datetime.now()
        formatted_date = now.strftime("%m/%d/%Y")
        formatted_time = now.strftime("%H:%M:%S")
        optimization_prompt = f"""
        You are a query generator. Given the following question, generate a simple search query.
        Date: {formatted_date}
        Time: {formatted_time}
        Question: {query}

        A proper search query will contain only the data requested, such as 'what was the score of the superbowl' or 'who just attacked Russia'.
        Your response must be a search query and nothing else. Provide ONLY a simple search query and nothing else in your response.

        """
        try:
            optimization_response = self.llm.generate([optimization_prompt])
            optimized_query = optimization_response.generations[0][0].text.strip()
            logging.info(f"Optimized Query: {optimized_query}")
            return optimized_query
        except Exception as e:
            logging.error(f"Error in query optimization: {e}")
            return query  # Fallback to the original query
