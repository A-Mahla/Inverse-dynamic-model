from vlm import VLM
from llm import LLM
import os
import sys
from annotation_manager import AnnotationManager, AnnotationMetadata

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from video_frames_creator.frame_manager import FrameManager


class Pipeline:
    """
    pipeline to generate annotations for frames
    """

    def __init__(self):
        self.df_frame_metadata = FrameManager.get_dataframe_metadata()
        self.vlm = VLM()
        self.llm = LLM()
        self.df_annotation_metadata = AnnotationManager.get_dataframe_metadata()

    def run(self):
        for _, row in self.df_frame_metadata.iterrows():
            if (
                row["frame_filename"]
                in self.df_annotation_metadata["frame_filename"].values
            ):
                print("Annotation already exists for frame:", row["frame_filename"])
                continue
            vlm_output = self.vlm.generate(row["frame_filename"])
            print(vlm_output)
            if "No software action found" in vlm_output:
                llm_output = '{ "annotation": {"error": "No software action found" } }'
            else:
                llm_output = self.llm.generate_(vlm_output)
            print(llm_output)
            annotation = AnnotationMetadata(
                frame_filename=row["frame_filename"],
                vlm_annotation=vlm_output,
                llm_json_annotation=llm_output,  # type: ignore
                title=row["title"],
                url=row["url"],
                software=row["software"],
            )
            df_new = AnnotationManager.create_dataframe(annotation)
            df_new.to_csv(
                AnnotationManager.get_metadata_file_path(),
                mode="a",
                header=False,
                index=False,
            )
            self.df_annotation_metadata = AnnotationManager.get_dataframe_metadata()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
