import yt_dlp
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def fetch_video_info(request):
    url = request.GET.get("url")
    
    if not url:
        return JsonResponse({"error": "Invalid URL"})

    ydl_opts = {
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        audio_streams = []
        video_streams = []

        for f in info.get("formats", []):
            # 🎵 Audio Only
            if f.get("acodec") != "none" and f.get("vcodec") == "none":
                bitrate = f.get("abr")
                bitrate_str = f"{bitrate} kbps" if bitrate else "Unknown kbps"
                audio_streams.append({
                    "bitrate": bitrate_str,
                    "url": f.get("url"),
                })

            # 🎥 Video with Audio (at least 720p)
            elif f.get("vcodec") != "none" and f.get("acodec") != "none":
                resolution = f.get("height")
                if resolution and resolution >= 360:  # Ensure 360p and above
                    resolution_str = f"{resolution}p"
                    video_streams.append({
                        "resolution": resolution_str,
                        "url": f.get("url"),
                    })

        # Sort video streams by resolution (highest first)
        video_streams.sort(key=lambda x: int(x["resolution"].replace("p", "")), reverse=True)

        data = {
            "title": info.get("title", "Unknown Title"),
            "thumbnail": info.get("thumbnail", ""),
            "audio_streams": audio_streams,
            "video_streams": video_streams,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)})





