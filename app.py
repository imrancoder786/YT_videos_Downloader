from flask import Flask, render_template, request
import yt_dlp
import datetime

app = Flask(__name__)

def get_video_info(link):
    try:
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "video")
            thumbnail = info.get("thumbnail")
            duration = str(datetime.timedelta(seconds=info.get("duration", 0)))

            formats = info.get("formats", [])

            video_formats = [
                {
                    "format_id": f.get("format_id"),
                    "resolution": f.get("format_note") or f.get("height"),
                    "ext": f.get("ext"),
                    "filesize": f.get("filesize"),
                    "url": f.get("url"),
                }
                for f in formats
                if f.get("ext") == "mp4" and f.get("acodec") != "none" and f.get("vcodec") != "none"
                and not f.get("format_note", "").startswith("DASH")
            ]

            audio_formats = sorted(
                [
                    {
                        "format_id": f.get("format_id"),
                        "ext": f.get("ext"),
                        "abr": f.get("abr"),
                        "filesize": f.get("filesize"),
                        "url": f.get("url")
                    }
                    for f in formats
                    if f.get("vcodec") == "none" and f.get("acodec") != "none" and f.get("abr")
                ],
                key=lambda x: abs(x["abr"] - 128)
            )[:1]

            return {
                "title": title,
                "thumbnail": thumbnail,
                "duration": duration,
                "video_formats": video_formats,
                "audio_formats": audio_formats
            }
    except Exception as e:
        print("Please Enter The Correct YouTube Link")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    video_data = None
    if request.method == 'POST':
        yt_link = request.form.get('yt_link')
        if yt_link:
            video_data = get_video_info(yt_link)
    return render_template('index.html', video_data=video_data)


if __name__ == '__main__':
    app.run(debug=True)
