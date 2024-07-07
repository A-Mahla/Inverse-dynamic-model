from typing import List
from pydantic import BaseModel
import os
import pandas as pd
import cv2
import sys
from frame_manager import FrameManager

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from video_scraper.video_manager import VideoManager, VideoMetadata, FrameMetadata


class VideoFrameMetaData(BaseModel):
    video_metadata: VideoMetadata
    frames_metadata: List[FrameMetadata]


class VideoFrameCreator:

    def __init__(self):
        if not os.path.exists(VideoManager.metadata_file_path):
            raise FileNotFoundError("Video Metadata file not found")
        self.video_metadata_file_path = VideoManager.metadata_file_path
        self.df_video_metadata = pd.read_csv(self.video_metadata_file_path)
        self.frame_output_dir = FrameManager.get_output_dir()
        self.frame_metadata_file_path = FrameManager.get_metadata_file_path()
        if os.path.exists(self.frame_metadata_file_path):
            self.df_frame_metadata = pd.read_csv(self.frame_metadata_file_path)
        else:
            self.df_frame_metadata = None

    def is_frame_exists(self, video_url: str) -> bool:
        if self.df_frame_metadata is None:
            return False
        return video_url in self.df_frame_metadata["url"].values

    def create_video_dataframes(self):
        os.makedirs(self.frame_output_dir, exist_ok=True)
        for _, row in self.df_video_metadata.iterrows():
            if self.is_frame_exists(row["url"]):
                print("Frames already exist for video:", row["title"])
                continue
            print("Processing video:", row["title"])
            frames_metadata = VideoManager.get_video_frame(row["title"])
            df = self.create_dataframe(
                VideoFrameMetaData(
                    video_metadata=VideoMetadata(**row.to_dict()),
                    frames_metadata=frames_metadata,
                )
            )
            for _, row in df.iterrows():
                cv2.imwrite(
                    f"{self.frame_output_dir}/{row['frame_filename']}",
                    row["frame"],
                )
            df.drop("frame", axis=1).to_csv(
                self.frame_metadata_file_path,
                mode="a",
                header=self.df_frame_metadata is None,
                index=False,
            )
            self.df_frame_metadata = pd.read_csv(self.frame_metadata_file_path)

    def create_dataframe(self, data: VideoFrameMetaData) -> pd.DataFrame:
        df = pd.DataFrame(
            [
                {
                    "url": data.video_metadata.url,
                    "title": data.video_metadata.title,
                    "language": data.video_metadata.language,
                    "width": data.video_metadata.width,
                    "height": data.video_metadata.height,
                    "ext": data.video_metadata.ext,
                    "software": data.video_metadata.software,
                    "duration": data.video_metadata.duration,
                    "frame": frame.frame,
                    "frame_number": frame.frame_number,
                    "frame_filename": frame.frame_filename,
                    "frame_time": frame.frame_time,
                }
                for frame in data.frames_metadata
            ]
        )
        return df


if __name__ == "__main__":
    VideoFrameCreator().create_video_dataframes()
