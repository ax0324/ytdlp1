from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import os

app = FastAPI(
    title="yt-dlp API",
    description="Return download URLs for video, audio, and cover image.",
    version="1.0.0",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "ax9657.@")

def verify_api_key(request: Request):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/api/info")
async def get_video_info(url: str, request: Request):
    verify_api_key(request)
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "description": info.get("description"),
            "thumbnail": info.get("thumbnail"),
            "formats": info.get("formats"),
            "webpage_url": info.get("webpage_url"),
        }

@app.get("/api/audio")
async def get_audio_url(url: str, request: Request):
    verify_api_key(request)
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        best_audio = next((f for f in info["formats"] if f.get("acodec") != "none" and f.get("vcodec") == "none"), None)
        return {
            "audio_url": best_audio["url"] if best_audio else None,
            "ext": best_audio["ext"] if best_audio else None
        }

@app.get("/api/cover")
async def get_cover(url: str, request: Request):
    verify_api_key(request)
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {"thumbnail": info.get("thumbnail")}