import os
import numpy as np
import pandas as pd
from PIL import Image


class FrameManager:

    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, "videoframes")
    frame_output_dir = os.path.join(output_dir, "frames")
    frame_metadata_file_path = os.path.join(output_dir, "videoframes_metadata.csv")

    @staticmethod
    def get_output_dir() -> str:
        os.makedirs(FrameManager.frame_output_dir, exist_ok=True)
        return FrameManager.frame_metadata_file_path

    @staticmethod
    def get_metadata_file_path() -> str:
        return FrameManager.frame_metadata_file_path

    @staticmethod
    def get_dataframe_metadata() -> pd.DataFrame:
        try:
            df = pd.read_csv(FrameManager.frame_metadata_file_path)
        except Exception:
            print("No frame metadata file found")
        return df

    @staticmethod
    def get_image_sample(frame_name: str) -> Image.Image:
        frame_path = f"{FrameManager.frame_output_dir}/{frame_name}"
        raw_image = Image.open(frame_path)
        return raw_image
