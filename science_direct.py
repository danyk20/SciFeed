import json

import requests

apiKey = 'a3d2594bffca21e891b47ec7009be4df'


def query_paper(query):
    headers = {}
    headers['Accept'] = 'application/json'
    headers['X-ELS-APIKey'] = 'a3d2594bffca21e891b47ec7009be4df'
    headers['Content-Type'] = 'application/json'


    base_url = " http://api.elsevier.com/content/search/sciencedirect"
    search_url = f"{base_url}?query=[{query}]&apiKey={apiKey}"

    try:
        response = requests.get(search_url, headers= headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    data = json.loads(response.content)
    paper_url = data['search-results']['entry'][0]['link'][1]['@href']
    return paper_url


if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    search_results = query_paper(search_query)

    if search_results:
        print("Search Results:")
        for idx, (title, link) in enumerate(search_results, 1):
            print(f"{idx}. {title}")
            print(f"   {link}\n")
    else:
        print("No results found.")
