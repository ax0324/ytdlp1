from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import os

app = FastAPI(
    title="yt-dlp Universal API",
    description="Return video/audio/cover download URLs for all supported platforms.",
    version="1.1.0",
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

def get_video_info_internal(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

@app.get("/api/info")
async def get_info(url: str, request: Request):
    verify_api_key(request)
    info = get_video_info_internal(url)
    return {
        "title": info.get("title"),
        "description": info.get("description"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "formats": info.get("formats"),
        "webpage_url": info.get("webpage_url"),
    }

@app.get("/api/audio")
async def get_audio_url(url: str, request: Request):
    verify_api_key(request)
    info = get_video_info_internal(url)
    audio = next((f for f in info["formats"] if f.get("vcodec") == "none" and f.get("acodec") != "none"), None)
    return {
        "audio_url": audio["url"] if audio else None,
        "ext": audio["ext"] if audio else None
    }

@app.get("/api/video")
async def get_video_url(url: str, request: Request):
    verify_api_key(request)
    info = get_video_info_internal(url)
    video = next((f for f in sorted(info["formats"], key=lambda x: x.get("height", 0), reverse=True)
                 if f.get("vcodec") != "none" and f.get("acodec") != "none" and f.get("url")), None)
    return {
        "video_url": video["url"] if video else None,
        "ext": video["ext"] if video else None,
        "quality": f'{video.get("height")}p' if video else None
    }

@app.get("/api/formats")
async def get_all_formats(url: str, request: Request):
    verify_api_key(request)
    info = get_video_info_internal(url)
    return {"formats": info.get("formats", [])}

@app.get("/api/cover")
async def get_cover(url: str, request: Request):
    verify_api_key(request)
    info = get_video_info_internal(url)
    return {"thumbnail": info.get("thumbnail")}
