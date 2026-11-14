
import time
from ddgs import DDGS


def search_web(
    query: str,
    max_results: int = 5,
    retries: int = 2,
    timeout: int = 15
) -> list:
    """
    Search the web using DuckDuckGo.

    Features:
    - Retries when a search fails.
    - Uses a longer timeout to handle slow responses.
    - Removes duplicate search results.
    - Returns an empty list if all attempts fail,
      allowing the investigation to continue.
    """

    # Validate the search query
    if not isinstance(query, str) or not query.strip():
        print("Web search skipped: Search query is empty.")
        return []

    # Validate the number of results
    if not isinstance(max_results, int) or max_results < 1:
        print("Invalid max_results. Using the default value of 5.")
        max_results = 5

    # Validate retry settings
    retries = max(1, retries)
    timeout = max(1, timeout)

    query = query.strip()

    print("\nSearching the web...")
    print(f"Search query: {query}")

    for attempt in range(1, retries + 1):

        try:
            print(
                f"Search attempt {attempt} "
                f"of {retries}..."
            )

            with DDGS(timeout=timeout) as ddgs:
                results = list(
                    ddgs.text(
                        query,
                        max_results=max_results
                    )
                )

            # Remove duplicate results using their URLs
            unique_results = []
            seen_urls = set()

            for result in results:

                if not isinstance(result, dict):
                    continue

                url = result.get("href") or result.get("url")

                if url:
                    if url in seen_urls:
                        continue

                    seen_urls.add(url)

                unique_results.append(result)

            print(
                f"Web search successful. "
                f"Found {len(unique_results)} results."
            )

            return unique_results

        except Exception as e:

            print(
                f"Search attempt {attempt} failed: "
                f"{type(e).__name__}: {e}"
            )

            if attempt < retries:
                wait_time = 2 * attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    # All attempts failed
    print("\nWeb search unavailable after all attempts.")
    print("Continuing investigation without web results.")

    return []
