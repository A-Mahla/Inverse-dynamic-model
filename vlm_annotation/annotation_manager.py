import os
import pandas as pd
from pydantic import BaseModel, Field


class AnnotationMetadata(BaseModel):
    frame_filename: str = Field(..., description="Frame filename")
    vlm_annotation: str = Field(..., description="VLM annotation")
    llm_json_annotation: str = Field(
        ..., description="LLM JSON annotation from VLM annotation"
    )
    title: str = Field(..., description="Video title")
    url: str = Field(..., description="URL")
    software: str = Field(..., description="Software name")


class AnnotationManager:

    base_dir = os.path.dirname(__file__)
    annotation_output_dir = os.path.join(base_dir, "annotation")
    annotation_metadata_file_path = os.path.join(
        annotation_output_dir, "frame_annotation_metadata.csv"
    )

    @staticmethod
    def get_output_dir() -> str:
        os.makedirs(AnnotationManager.annotation_output_dir, exist_ok=True)
        return AnnotationManager.annotation_output_dir

    @staticmethod
    def get_metadata_file_path() -> str:
        return AnnotationManager.annotation_metadata_file_path

    @staticmethod
    def get_dataframe_metadata() -> pd.DataFrame:
        try:
            df = pd.read_csv(AnnotationManager.annotation_metadata_file_path)
        except Exception:
            AnnotationManager.get_output_dir()
            df = pd.DataFrame(
                columns=[
                    "frame_filename",
                    "vlm_annotation",
                    "llm_json_annotation",
                    "title",
                    "url",
                    "software",
                ]
            )
            df.to_csv(AnnotationManager.annotation_metadata_file_path, index=False)
        return df

    @staticmethod
    def create_dataframe(data: AnnotationMetadata) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "frame_filename": [data.frame_filename],
                "vlm_annotation": [data.vlm_annotation],
                "llm_json_annotation": [data.llm_json_annotation],
                "title": [data.title],
                "url": [data.url],
                "software": [data.software],
            }
        )
