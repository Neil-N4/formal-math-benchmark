from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    claim_id: str
    statement: str
    formalizable: bool
    lean_name: str
    match_terms: tuple[str, ...]


@dataclass(frozen=True)
class Problem:
    problem_id: str
    source: str
    topic: str
    difficulty: str
    prompt: str
    final_answer: str
    solution_skeleton: tuple[Claim, ...]


@dataclass(frozen=True)
class Response:
    problem_id: str
    final_answer: str
    claims: tuple[str, ...]


@dataclass(frozen=True)
class ModelRun:
    model: str
    prompt_style: str
    responses: tuple[Response, ...]
