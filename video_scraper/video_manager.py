import pandas as pd
import pandas as pd
from pydantic import BaseModel, Field, field_validator, validator
from typing import List, Optional
import os
import cv2


class VideoMetadata(BaseModel):
    url: str = Field(..., title="URL of the video")
    title: str = Field(default="", title="Title of the video")
    width: int = Field(default=0, title="Width of the video")
    height: int = Field(default=0, title="Height of the video")
    language: Optional[str] = Field(default=None, title="Language of the video")
    ext: str = Field(..., title="Extension of the video")
    software: str = Field(..., title="Software used to download the video")
    duration: float = Field(default=0.0, title="Duration of the video in seconds")

    @field_validator("title", mode="before")
    def validate_title(cls, value, field):
        if value is None:
            return "no language"
        return value

    @field_validator("language", mode="before")
    def validate_language(cls, value, field):
        if value is None:
            return "no language"
        return value

    @field_validator("width", "height", mode="before")
    def validate_integer(cls, value, field):
        if value is None:
            return 0
        return value

    @field_validator("duration", mode="before")
    def validate_float(cls, value, field):
        if value is None:
            return 0.0
        return value


class FrameMetadata(BaseModel):
    frame: cv2.typing.MatLike = Field(..., title="Frame")
    frame_number: float = Field(..., title="Frame number")
    frame_filename: str = Field(..., title="Filename of the frame")
    frame_time: float = Field(default=0.0, title="Time of the frame in seconds")

    class Config:
        arbitrary_types_allowed = True


class VideoManager:

    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, "downloads")
    output_dir_video = os.path.join(output_dir, "videos")
    metadata_file_path = os.path.join(output_dir, "video_metadata.csv")

    @staticmethod
    def get_output_dir() -> str:
        os.makedirs(VideoManager.output_dir_video, exist_ok=True)
        return VideoManager.output_dir_video

    @staticmethod
    def get_metadata_file_path() -> str:
        return VideoManager.metadata_file_path

    @staticmethod
    def get_download_video_metadata() -> pd.DataFrame:
        try:
            df = pd.read_csv(VideoManager.metadata_file_path)
        except Exception:
            print("No metadata file found")
        return df

    @staticmethod
    def get_video_frame(
        video_name: str,
    ) -> List[FrameMetadata]:
        video_path = f"{VideoManager.output_dir_video}/{video_name}"
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError("Error: Could not open video.")
        fps = video.get(cv2.CAP_PROP_FPS)
        interval = int(fps * 2)
        frames = []
        while True:
            ret, frame = video.read()
            if not ret:
                break
            frame_number = video.get(cv2.CAP_PROP_POS_FRAMES)
            frames.append(
                FrameMetadata(
                    frame=frame,
                    frame_number=frame_number,
                    frame_filename=f"{video_name.replace(' ', '_')}_frame_{int(frame_number)}.jpg",
                    frame_time=video.get(cv2.CAP_PROP_POS_MSEC),
                )
            )
            video.set(
                cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES) + interval
            )
        return frames
