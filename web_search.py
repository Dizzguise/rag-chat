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
            logging.info(f"Requesting Brave API with query: {query}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            logging.info(f"Raw results: {results}")

            # Extract snippets from various possible fields
            web_results = []
            if 'web' in results and isinstance(results['web'], dict):
                if 'results' in results['web']:
                    for item in results['web']['results']:
                        if 'description' in item:
                            web_results.append(item['description'])
                        elif 'extra_snippets' in item:
                            web_results.append(item['extra_snippets'][0])
                        else:
                            web_results.append(item['url'])  # fallback to URL if no description or snippet

            logging.info(f"Web results: {web_results}")
            return web_results
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during web search: {e}")
            return []

# Configure logging
logging.basicConfig(level=logging.DEBUG)
