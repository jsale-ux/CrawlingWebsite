# This script scrapes a Wikipedia page to extract the title, first 3 paragraphs, and section headings.
# It captures both the content of the article and how it is structured.

# -------------------- SECTION 1: IMPORTS --------------------
# We import the libraries needed to send a web request and parse HTML content
import requests  # used to send HTTP request to the website
from bs4 import BeautifulSoup  # used to parse and extract HTML content


# -------------------- SECTION 2: SET URL AND HEADERS --------------------
# We define the webpage we want to scrape and include a User-Agent to act like a browser
url = "https://en.wikipedia.org/wiki/Web_scraping"

# These are HTTP headers sent with the request to identify the client (e.g., browser), not page content.
# They are different from HTML headings (h1, h2, h3), which are extracted later from the webpage.
headers = {
    "User-Agent": "Mozilla/5.0"  # makes request look like it comes from a browser so it is not blocked
}

# -------------------- SECTION 3: SEND REQUEST --------------------
# We send a request to the website and retrieve the HTML content
response = requests.get(url, headers=headers, timeout=10)  # fetch page HTML
response.raise_for_status()  # stops the program if the request fails (e.g., page not found)


# -------------------- SECTION 4: PARSE HTML --------------------
# We convert raw HTML into a structured format so Python can navigate it easily
soup = BeautifulSoup(response.text, "lxml")
# response.text = raw HTML of the page
# "lxml" = parser that helps interpret HTML structure


# -------------------- SECTION 5: EXTRACT TITLE --------------------
# We locate and print the main page title from the <h1> tag
title = soup.find("h1").text.strip()
# .find("h1") gets the first h1 tag
# .text extracts visible text
# .strip() removes extra spaces or line breaks
print("Title:", title)


# -------------------- SECTION 6: GET MAIN CONTENT --------------------
# We isolate the main article section to avoid scraping menus or sidebars
content = soup.find("div", {"id": "mw-content-text"})
# this targets only the article body where useful information exists


# -------------------- SECTION 7: FIRST 3 PARAGRAPHS --------------------
# We extract and print the first 3 meaningful paragraphs from the article
paragraphs = content.find_all("p")
# find_all returns a list of all paragraph tags

print("\nFirst 3 paragraphs:\n")

count = 0
for p in paragraphs:
    text = p.text.strip()  # extract text and clean whitespace

    if text:  # ignore empty paragraphs
        print(text, "\n")
        count += 1

    if count == 3:
        break  # stop after printing 3 valid paragraphs


# -------------------- SECTION 8: HEADINGS --------------------
# We extract and print all main headings (h2) and subheadings (h3)
print("\nHeadings and Subheadings:\n")

headings = content.find_all(["h2", "h3"])
# find all section headings and subsection headings

for heading in headings:
    text = heading.get_text(" ", strip=True)
    # get_text extracts text and joins parts with spaces

    text = text.replace("[edit]", "").strip()
    # removes Wikipedia's "[edit]" label for cleaner output

    print(text)