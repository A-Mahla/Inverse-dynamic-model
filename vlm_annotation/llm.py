import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from vlm_annotation.prompts import llm_prompt
from pydantic import BaseModel, Field
from typing import Literal
import json
from outlines.generate.regex import regex
from outlines.fsm.json_schema import build_regex_from_schema
from outlines.models.transformers import Transformers


class Annotation(BaseModel):
    software: str = Field(..., description="Software name")
    accuracy: float = Field(
        ...,
        description="Percentage accuracy of software name found in decimal format (for example, 0.95) between 0 and 1",
    )
    features_used: str = Field(..., description="Description of features or tools used")
    past_actions: str = Field(..., description="Description of past actions")
    future_actions: str = Field(..., description="Predictions about future actions")


class AnnotationError(BaseModel):
    error: Literal["No software action found"] = Field(
        ..., description="No software action found"
    )


class AnnotationGuidedSchema(BaseModel):
    annotation: Annotation | AnnotationError


class LLM:

    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
        self.prompt = llm_prompt
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.generator = regex(
            Transformers(self.model, self.tokenizer),  # type: ignore
            build_regex_from_schema(
                json.dumps(AnnotationGuidedSchema.model_json_schema())
            ),
        )

    def generate_(self, vlm_output: str):
        message = [
            {"role": "user", "content": llm_prompt.format(vlm_output=vlm_output)},
        ]
        prompt_template = self.tokenizer.apply_chat_template(
            message, add_generation_prompt=True, return_tensors="pt", tokenize=False
        )
        if not isinstance(prompt_template, str):
            raise ValueError("Prompt template is not a string")
        output = self.generator(prompt_template)
        return output
