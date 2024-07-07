from yt_dlp import YoutubeDL
import pandas as pd
import os
from video_url import video_url
from video_manager import VideoManager, VideoMetadata
from typing import Optional
import re

# Youtube video scaper to create a dataset


class YoutubeScraper:
    """
    This class is used to download youtube videos and store the metadata in a csv file
    """

    def __init__(self, video_url: dict[str, str]):
        self.output_dir = VideoManager.get_output_dir()
        self.output_csv_file = VideoManager.get_metadata_file_path()
        os.makedirs(self.output_dir, exist_ok=True)
        self.video_url = video_url
        try:
            self.df = pd.read_csv(self.output_csv_file)
        except Exception:
            print("Creating new file dataframe")
            self.df = pd.DataFrame(
                columns=[field for field in VideoMetadata.model_fields.keys()]
            )

    def get_ydl_opts(self, filename: Optional[str] = None) -> dict:
        ydl_opts = {
            "outtmpl": os.path.join(f"{self.output_dir}", f"{filename}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
            "noplaylist": True,
        }
        if filename is None:
            ydl_opts.pop("outtmpl")
        return ydl_opts

    def get_video_info_name(self, key: str) -> Optional[str]:
        with YoutubeDL(self.get_ydl_opts()) as yt:
            try:
                info = yt.extract_info(key, download=False)
                if info is None:
                    return None
                sanitized_title = YoutubeScraper.sanitize_filename(info["title"])
                return sanitized_title
            except Exception as e:
                print(f"Error downloading info name {key}: {e}")
                return None

    def download_video(self):
        for key, value in self.video_url.items():
            if key in self.df["url"].values:
                print(f"Skipping {key} as it is already downloaded")
                continue
            sanitized_title = self.get_video_info_name(key)
            if sanitized_title is None:
                continue
            with YoutubeDL(self.get_ydl_opts(filename=sanitized_title)) as yt:
                try:
                    info = yt.extract_info(key, download=False)
                    if info is None:
                        continue
                    yt.download([key])
                except Exception as e:
                    print(f"Error downloading {key}: {e}")
                    continue
                # ext = info.get("ext", None)
                ext = "mp4"
                metadata = VideoMetadata(
                    url=key,
                    title=f"{sanitized_title}.{ext}",
                    width=int(info.get("width", 0)),
                    height=int(info.get("height", 0)),
                    language=info.get("language", "no language"),
                    ext=ext,
                    software=value,
                    duration=float(info.get("duration", 0)),
                )
                new_row = pd.DataFrame([metadata.model_dump()])
                self.df = pd.concat([self.df, new_row], ignore_index=True)
                self.df.to_csv(self.output_csv_file, index=False)

    @staticmethod
    def sanitize_filename(filename: str):
        """
        Sanitizes a string to be safe as a filename by removing or replacing characters
        that are not alphanumeric, dashes, or underscores.
        """
        sanitized = re.sub(r"[^\w\s-]", "_", filename)
        sanitized = re.sub(r"[\s-]+", "_", sanitized)
        sanitized = sanitized.strip("_ ")
        return sanitized


if __name__ == "__main__":
    yt = YoutubeScraper(video_url)
    yt.download_video()
    print("Download completed")
