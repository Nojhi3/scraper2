from fastapi import FastAPI, Query, BackgroundTasks
import requests
from pydantic import BaseModel
from typing import List, Dict
import together 
import os
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import asyncio
import re

app = FastAPI()

youtube_api = "AIzaSyAmt734ugZJiigg7C3VAzZLLJ3iKR1GrHc"
together_api = os.getenv("TOGETHER_API_KEY")
if not together_api:
    raise ValueError("TOGETHER_API_KEY environment variable is not set!")
google_api = "AIzaSyAmt734ugZJiigg7C3VAzZLLJ3iKR1GrHc"
google_cse_id = "734a723e5c2d64e81"



client = together.Together(api_key=together_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str

async def google_search(query: str) -> List[Dict[str, str]]:
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api}&cx={google_cse_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            data = await response.json()
            print(f"🔍 Google API Response: {data}")  # ✅ Debugging
    return [{"title": item.get("title", "No Title"), "link": item.get("link", "No Link")} for item in data.get("items", [])]

async def youtube_search(query: str) -> List[Dict[str, str]]:
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={youtube_api}"
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            data = await response.json()
    return [{"title": item["snippet"].get("title", "No Title"), "link": f"https://www.youtube.com/watch?v={item['id'].get('videoId', '')}"} for item in data.get("items", []) if "videoId" in item.get("id", {})]

async def summarize_texts(texts: List[str]):
    if not texts:
        return []
    prompt = "Summarize these search results:\n" + "\n".join(texts)
    response = await asyncio.to_thread(client.chat.completions.create,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    summaries = response.choices[0].message.content.strip().split("\n")
    return summaries if summaries else ["No summary available"] * len(texts)

async def rank_results(query: str, results: List[Dict[str, str]]):
    if not results:
        return []
    tasks = []
    for result in results:
        tasks.append(
            asyncio.to_thread(client.chat.completions.create,
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                messages=[{"role": "user", "content": f"Rate the relevance of this result to '{query}' on a scale of 1-10. Only return the number: {result.get('title', 'No Title')} - {result.get('link', 'No Link')}"}],
            )
        )
    responses = await asyncio.gather(*tasks)
    scored_results = []
    for result, response in zip(results, responses):
        score = 5  # Default score
        try:
            match = re.search(r'(\d+)', response.choices[0].message.content)
            if match:
                score = min(10, max(1, int(match.group(1))))
        except Exception as e:
            print(f"Error processing ranking: {e}")
        scored_results.append({"title": result.get("title", "No Title"), "link": result.get("link", "No Link"), "score": score})
    return sorted(scored_results, key=lambda x: x["score"], reverse=True)

@app.post("/search")
async def search(data: SearchQuery, background_tasks: BackgroundTasks):
    print(f"🔍 Received Query: {data.query}")  # ✅ Debugging

    google_task = asyncio.create_task(google_search(data.query))
    youtube_task = asyncio.create_task(youtube_search(data.query))
    
    google_results, youtube_results = await asyncio.gather(google_task, youtube_task)

    print(f"📌 Google Results: {google_results}")  # ✅ Debugging
    print(f"📌 YouTube Results: {youtube_results}")  # ✅ Debugging

    if not google_results and not youtube_results:
        return {"error": "No results found"}

    results = {"google": google_results, "youtube": youtube_results}

    ranked_results = await rank_results(data.query, google_results + youtube_results)
    results["ranked"] = ranked_results

    print(f"✅ Final Ranked Results: {ranked_results}")  # ✅ Debugging

    return {"query": data.query, "results": results}
