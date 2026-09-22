import os
import re
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
from rich import print
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

#  Tavily Client 
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("Thiếu TAVILY_API_KEY trong file .env!")

tavily = TavilyClient(api_key=tavily_api_key)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    try:
        results = tavily.search(query=query, max_results=5)
        out = []
        for r in results.get("results", []):
            title = r.get("title", "No Title")
            url = r.get("url", "")
            snippet = r.get("content", "")[:300]
            out.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")

        return "\n---\n".join(out) if out else "No results found."
    except Exception as e:
        return f"Error during web search: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and extract clean readable content from a URL. Uses multiple extraction strategies for better reliability."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # 1. Fetch web page
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # Strategy 1: trafilatura (tối ưu cho bài báo/tin tức)
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
        )
        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", extracted)
            return cleaned[:5000]

        # Strategy 2: readability-lxml + BeautifulSoup
        doc = Document(html)
        clean_html = doc.summary()
        soup = BeautifulSoup(clean_html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        if text and len(text.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", text)
            return cleaned[:5000]

        # Strategy 3: fallback bóc tách toàn trang HTML gốc
        soup_fallback = BeautifulSoup(html, "html.parser")
        for tag in soup_fallback(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        fallback_text = soup_fallback.get_text(separator=" ", strip=True)
        cleaned_fallback = re.sub(r"\s+", " ", fallback_text)
        if cleaned_fallback:
            return cleaned_fallback[:5000]

        return "Could not extract meaningful content from the page."

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"