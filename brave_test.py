import logging
import requests

class WebSearch:
    def __init__(self, api_key, count=10, extra_snippets=True):
        self.api_key = api_key
        self.count = count
        self.extra_snippets = extra_snippets

    def search(self, query):
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        params = {
            "q": query,
            "extra_snippets": str(self.extra_snippets).lower(),
            "count": self.count
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            logging.info(f"Raw results: {results}")

            # Log the structure of the JSON response to understand what fields are returned
            for key in results.keys():
                logging.info(f"Result field: {key}, Type: {type(results[key])}")

            # Extract snippets from various possible fields
            web_results = []
            if 'web' in results and isinstance(results['web'], dict):
                if 'results' in results['web']:
                    web_results.extend(item.get('description', '') for item in results['web']['results'])
            if 'mixed' in results:
                for section in ['main', 'top', 'side']:
                    if section in results['mixed']:
                        web_results.extend(item.get('description', '') for item in results['mixed'][section])
            logging.info(f"Web results: {web_results}")
            return web_results
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during web search: {e}")
            return []

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# API key and query
api_key = 'BSA0fWObRoWqALPixFw4raPLCKXpB6c'
query = "mavericks game score -06/06/2024"

# Perform the search
web_search = WebSearch(api_key)
results = web_search.search(query)

# Print the results
print("Web search results:")
for result in results:
    print(result)
