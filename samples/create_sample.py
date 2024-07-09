import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from vlm_annotation.annotation_manager import AnnotationManager


def generate_markdown_from_dataframe():
    df = AnnotationManager.get_dataframe_metadata()

    random_rows = df.sample(n=50, random_state=11)
    if os.path.exists("output.md"):
        os.remove("output.md")
    with open("output.md", "w") as file:
        for index, row in random_rows.iterrows():
            title = row["title"]
            frame_filename = row["frame_filename"]
            vlm_annotation = row["vlm_annotation"]
            llm_json_annotation = json.dumps(
                json.loads(row["llm_json_annotation"]), indent=4
            )

            file.write(f"<br>\n\n## Title (video file name): {title}\n")
            file.write(f"### Frame filename: {frame_filename}\n\n")
            file.write(
                f"![Image](../video_frames_creator/videoframes/frames/{frame_filename})\n\n"
            )
            file.write(f"<br>\n\n**VLM annotation**: \n*{vlm_annotation}*\n")
            file.write(
                f"<br>\n\n**LLM Json annotation**: \n```\n{llm_json_annotation}\n```\n\n"
            )
            file.write("---\n\n")


if __name__ == "__main__":
    generate_markdown_from_dataframe()
