import re

from pytube import YouTube as PyYoutube


RE_YOUTUBE_URL_PATTERN = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?(?=.*v=\w+)(?:\S+)?|embed\/|v\/|attribution_link\?a=)([\w\d]+)|youtu\.be\/([\w\d]+))"


class YoutubeBase:
    def download_video(
        self,
        url: str,
        with_highest_res: bool = True,
        with_first: bool = False,
        file_format: str = "mp4",
        saved_file_path: str = "./",
    ) -> None:
        if not is_youtube_url(url):
            raise Exception("Invalid youtube url")

        yt = PyYoutube(
            url,
            use_oauth=True,
            on_progress_callback=lambda: print("downloading..."),
            on_complete_callback=lambda: print("download completed"),
            allow_oauth_cache=True,
        )

        if with_highest_res:
            yt.streams.filter(progressive=True, file_extension=file_format).order_by(
                "resolution"
            ).desc().first().get_audio_only().download(saved_file_path)

        elif with_first:
            yt.streams.first().download(saved_file_path)


def is_youtube_url(url: str) -> bool:
    return bool(re.match(RE_YOUTUBE_URL_PATTERN, url))
