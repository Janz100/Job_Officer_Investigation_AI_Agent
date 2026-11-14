from tools.web_search import search_web

print("Testing web search...")

results = search_web(
    "ABC Technologies company information",
    max_results=3
)

if results:
    print("\nSearch successful!")
    for result in results:
        print("\nTitle:", result.get("title"))
        print("URL:", result.get("href"))
        print("Description:", result.get("body"))
else:
    print("\nNo search results available.")