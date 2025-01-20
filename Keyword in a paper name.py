import requests
from datetime import datetime
import time

def get_publication_count_by_year_in_title(keyword, start_year=2000):
    url = "https://api.crossref.org/works"
    current_year = datetime.now().year
    results = {}

    for year in range(start_year, current_year + 1):
        params = {
            'query.title': keyword,  # Focus search on titles
            'filter': f'from-pub-date:{year}-01-01,until-pub-date:{year}-12-31',
            'rows': 0  # We only need the count
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            total_results = data['message']['total-results']
            results[year] = total_results
            print(f"{year}: {total_results}")
        else:
            print(f"Failed to fetch data for {year}. Status code: {response.status_code}")
            results[year] = None

        # Avoid hitting rate limits
        time.sleep(1)

    return results

# Example usage
publication_counts_title_only = get_publication_count_by_year_in_title("macro-prudential")
