import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
import wikipedia

def find_articles(topic):
    query = topic.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}+site:wikipedia.org"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    links = []

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            href = a['href']
            if "url?q=" in href and "wikipedia.org" in href:
                clean_link = href.split("url?q=")[1].split("&")[0]
                if clean_link not in links:
                    links.append(clean_link)
            if len(links) >= 2:
                break
    except Exception as e:
        print("Search error:", e)

    # Fallback if scraping failed
    if len(links) < 2:
        try:
            search_results = wikipedia.search(topic)
            for result in search_results:
                page_url = f"https://en.wikipedia.org/wiki/{result.replace(' ', '_')}"
                if page_url not in links:
                    links.append(page_url)
                if len(links) >= 2:
                    break
        except Exception as e:
            print("Wikipedia fallback failed:", e)

    return {
        "basic": links[0] if len(links) > 0 else "https://en.wikipedia.org/wiki/General_knowledge",
        "depth": links[1] if len(links) > 1 else "https://en.wikipedia.org/wiki/Knowledge"
    }


def find_youtube_videos(topic):
    videos_search = VideosSearch(topic, limit=5)
    results = videos_search.result()['result']

    basic_video = ""
    depth_video = ""

    for video in results:
        title = video['title'].lower()
        if 'introduction' in title or 'basics' in title or 'for beginners' in title:
            basic_video = video['link']
        elif 'deep' in title or 'in depth' in title or 'intermediate' in title:
            depth_video = video['link']

        if basic_video and depth_video:
            break

    return {
        "basic": basic_video if basic_video else results[0]['link'],
        "depth": depth_video if depth_video else results[1]['link']
    }
