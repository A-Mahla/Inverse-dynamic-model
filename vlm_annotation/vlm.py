import os
import sys
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from prompts import vlm_prompt

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from video_frames_creator.frame_manager import FrameManager


class VLM:

    def __init__(self, model_name="llava-hf/llava-1.5-13b-hf"):
        self.prompt = vlm_prompt
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = LlavaForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(0)

    def generate(self, frame_name: str):
        raw_image = FrameManager.get_image_sample(frame_name)
        prompt_template, prompt_length = VLM.apply_prompt_template(self.prompt)
        inputs = self.processor(prompt_template, raw_image, return_tensors="pt").to(0)
        outputs = self.model.generate(**inputs, max_new_tokens=200, do_sample=False)
        return self.processor.decode(outputs[0], skip_special_tokens=True)[
            prompt_length:
        ]

    @staticmethod
    def apply_prompt_template(prompt: str):
        prompt_lenght_without_image = len(f"USER: \n{prompt}\nASSISTANT:") + 2
        return f"USER: <image>\n{prompt}\nASSISTANT:", prompt_lenght_without_image


class Action:
    action: str
