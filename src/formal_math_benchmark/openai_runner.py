from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OpenAIConfig:
    model: str
    api_key_env: str = "OPENAI_API_KEY"


PROMPT_TEMPLATE = """You are solving a competition-style math problem.

Return JSON with this schema:
{
  "final_answer": "string",
  "claims": ["step 1", "step 2", "step 3"]
}

Problem:
{problem}
"""


def collect_response(problem: str, config: OpenAIConfig) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install the optional 'openai' dependency to use OpenAI collection.") from exc

    api_key = os.environ.get(config.api_key_env)
    if not api_key:
        raise RuntimeError(f"Missing API key in environment variable {config.api_key_env}.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=config.model,
        input=PROMPT_TEMPLATE.format(problem=problem),
    )
    return {"raw_text": response.output_text}
