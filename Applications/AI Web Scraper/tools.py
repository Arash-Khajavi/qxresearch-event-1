from langchain.tools import Tool
from datetime import datetime
from langchain_core.utils.pydantic import BaseModel
from langchain_openai.chat_models  import ChatOpenAI
from langchain.agents import create_tool_calling_agent
# Example of a Pydantic model for the tool
from langchain_core.tools import tool
from pydantic import BaseModel
from langchain_core.tools import tool
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup  # ✅ Correct
# Define the argument schema for the tool
from langchain.tools import Tool
from datetime import datetime
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)


# print(data)
# if __name__ == "__main__":
#     tool = SearchMHG()
#     result = tool.invoke("fetch mhg.html data")
#     print(result)

    # Print a preview of the first 500 chars of each page for debugging
    # data = SearchMHG()
    # print(data)
    # for page_name, info in data.items():

    #     if "full_text" in info:
    #         print(info["full_text"])
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import re
from langchain.tools import BaseTool
# def info_m():
#     #    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        filehandle = open('mhg.html')
#     # formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

#     #    b=open(filename, "a", encoding="utf-8")
#     #    resp = requests.get(filename)
#     #    print(f"Requests status code: {resp.status_code}")
#     #    print(resp.text[:500])  # first 500 chars for debugging
#        n=str(filehandle).find("<body>")
#        n1=str(filehandle).find("</html>")
#        soup = BeautifulSoup(str(filehandle)[n:n1],'html.parser')
#        print(f"scraped successfully {soup}")
# print(info_m())
# class SearchMSG(BaseTool):
#     name: str='mhg.html'
#     description: str='Scrapes through the mhg.html file and extracts data'
#     def _run(self, query: str) -> str:
#         """Scrapes through the mhg.html file and extracts data"""
#         info_m()
#         return "Scrapes through the mhg.html file and extracts data"

#     # async def _arun(self, query: str) -> str:
#     #     raise NotImplementedError("Async not supported")
# sav= Tool(
#     name="extract extra info",
#     func=info_m(),
#     description=" Collects data from the mhg.html file",
# )
# print(SearchMSG)
# ---------------------------------------
# Scraper functions with debug prints
# ---------------------------------------

# def fetch_with_requests(url: str='https://www.jbschool.ae/'):
#     try:
#         resp = requests.get(url)
#         resp.raise_for_status()
#         print(f"✅ Requests status code: {resp.status_code}")
       
#         response=requests.get(url)
#         print(resp.text[:500])  # first 500 chars for debugging
#         soup = BeautifulSoup(resp.text, "html.parser")
#         if len(soup.get_text(strip=True)) > 200:
#             print("Requests content seems OK")
#             return soup
#         else:
#             print("⚠️ Requests content too short, fallback to JS")
#             return None
#     except Exception as e:
#         print(f"❌ Requests failed: {e}")
#         return None

def fetch_with_playwright(url: str):
    with sync_playwright() as p:
        # Launch headless (no browser UI)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0 Safari/537.36"
        ))
        page = context.new_page()

        # Load only until DOM is ready (faster, avoids timeouts)
        page.goto(url)

        # Grab page content
        html = page.content()

        browser.close()
        return BeautifulSoup(html, "html.parser")

# Example usage
soup = fetch_with_playwright("https://www.carfax-education.com/")

def fetch_page(url: str='"https://www.carfax-education.com/"'):

    soup = fetch_with_playwright(url)
    return soup
# print(fetch_page())
# ---------------------------------------
# Structured extraction
# ---------------------------------------

def extract_structured_info(soup):
    text = soup.get_text(separator="\n", strip=True)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s-]{7,}\d", text)
    steps = [h.get_text(strip=True) for h in soup.find_all("h2") if "STEP" in h.get_text(strip=True).upper()]
    return {
        "full_text": text,
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "steps": steps
    }

# ---------------------------------------
# Scrape multiple pages
# ---------------------------------------
from datetime import time
def scrape_aquila():
    """Search My PORN website to fetch data on sexual videos """
    base = "https://www.carfax-education.com/"
    pages = {
        'guardianship': 'guardianship',
        'admissions': 'admissions', 
        'programs': 'programs',
        'tuition-fees': 'tuition-fees',     
        'contact': 'contact',
        'about-us': 'about-us',
        'faq': 'faq',
        'news': 'news',
        'events': 'events',
        'careers': 'careers',
        'resources': 'resources',
        'alumni': 'alumni',
        'tutors': 'tutors',
        'privacy-policy': 'privacy-policy',
    }
    data = {}
    for name, path in pages.items():
        url = base+path
        print(f"\n--- Fetching  page ---")
        soup = fetch_page(url)
        if soup:
                if soup.title:
                    info = {"title": soup.title.string}
                    info.update(extract_structured_info(soup))
                    data[url] = info
    # Save to JSON
                    with open("aquila_data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                    print("📂 Data saved to aquila_data.json")
                    return data
# print(scrape_aquila())
# print(scrape_aquila())
# ---------------------------------------
# LangChain Tool wrapper
# ---------------------------------------
class AquilaTool(BaseTool):
    name: str = "aquila_scraper"
    description: str = """Use this tool to search Carfax-Education's official website for information. """
    def _run(self, query: str) -> str:
        """Searches scraped Crafx-Education data for the query and returns relevant information."""
        import json
        import os
        import re
        json_path = "aquila_data.json"
        
        # Scrape if JSON doesn't exist or is empty
        if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
            print("Scraping data as JSON is missing or empty...")
            scrape_aquila()
        
        # Load the data
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Improved keyword extraction
        clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
        words = [w.strip() for w in clean_query.split() if w.strip()]
        common_words = {'does', 'offer', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had', 'do', 'did', 'but', 'or', 'and', 'not', 'can', 'could', 'would', 'should'}
        keywords = [w for w in words if w not in common_words and len(w) > 2]
        # Split hyphens
        expanded_keywords = []
        for k in keywords:
            expanded_keywords.append(k)
            if '-' in k:
                expanded_keywords.extend(k.split('-'))
        keywords = list(set(expanded_keywords))
        
        relevant_info = []
        for page_name, page_data in data.items():
            if "full_text" in page_data:
                full_text = page_data["full_text"].lower()
                if any(k in full_text for k in keywords):
                    # Find best match position
                    best_start = -1
                    best_keyword = ""
                    for k in keywords:
                        pos = full_text.find(k)
                        if pos > best_start:
                            best_start = pos
                            best_keyword = k
                    if best_start != -1:
                        snippet = page_data["full_text"][max(0, best_start-200):best_start+600].strip()
                        relevant_info.append(f"Source: {page_name}\nSnippet: {snippet}\n---")
        
        if relevant_info:
            return "Relevant information found:\n" + "\n".join(relevant_info)
        else:
            return "No relevant data found in the scraped Carfax-education pages for this query."

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")

if __name__ == "__main__":
    tool = AquilaTool()
    result = tool.invoke("fetch Carfax  data")
    print(result)

    # Print a preview of the first 500 chars of each page for debugging
    data = scrape_aquila()
    for page_name, info in data.items():
        print(f"\n=== {page_name} ===")
        if "full_text" in info:
            print(info["full_text"])
            pass
        else:
            # print(info)
            pass
