
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def check_website(url: str) -> dict:
    """
    Check website accessibility and collect basic technical details.

    Checks:
    - URL format
    - Website accessibility
    - HTTP status code
    - HTTPS usage
    - Page title
    - Redirected URL

    Important:
    Website accessibility does not prove that a company
    is legitimate or that a recruiter is authorized.
    """

    # 1. Validate empty input
    if not isinstance(url, str) or not url.strip():
        return {
            "accessible": False,
            "error": "No valid website URL provided."
        }

    url = url.strip()

    # 2. Add HTTPS if the user did not provide a protocol
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # 3. Validate URL structure
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        if (
            parsed.scheme not in ("http", "https")
            or not hostname
            or "." not in hostname
            or " " in hostname
        ):
            return {
                "original_url": url,
                "accessible": False,
                "error": "Invalid website URL."
            }

    except ValueError:
        return {
            "original_url": url,
            "accessible": False,
            "error": "Invalid website URL."
        }

    # 4. Check website accessibility
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        # 5. Extract basic webpage information
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "No title found"
        )

        # 6. Get final URL after redirects
        final_url = response.url
        final_parsed = urlparse(final_url)

        return {
            "original_url": url,
            "final_url": final_url,
            "domain": final_parsed.hostname,
            "status_code": response.status_code,
            "accessible": response.status_code < 400,
            "uses_https": final_parsed.scheme == "https",
            "page_title": title,
            "warning": (
                "Website accessibility does not prove "
                "company legitimacy or recruiter identity."
            )
        }

    # 7. Handle connection errors
    except requests.exceptions.Timeout:
        return {
            "original_url": url,
            "accessible": False,
            "error": "Website request timed out."
        }

    except requests.exceptions.ConnectionError:
        return {
            "original_url": url,
            "accessible": False,
            "error": "Could not connect to the website."
        }

    except requests.exceptions.RequestException as e:
        return {
            "original_url": url,
            "accessible": False,
            "error": str(e)
        }

    except Exception as e:
        return {
            "original_url": url,
            "accessible": False,
            "error": f"Unexpected error: {str(e)}"
        }
