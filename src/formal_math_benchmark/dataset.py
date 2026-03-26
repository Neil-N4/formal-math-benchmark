from __future__ import annotations

import json
from pathlib import Path

from .models import Claim, ModelRun, Problem, Response


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_benchmark(path: Path | None = None) -> tuple[Problem, ...]:
    benchmark_path = path or _project_root() / "data" / "problems.json"
    payload = json.loads(benchmark_path.read_text())
    problems: list[Problem] = []
    for item in payload:
        skeleton = tuple(
            Claim(
                claim_id=claim["claim_id"],
                statement=claim["statement"],
                formalizable=claim["formalizable"],
                lean_name=claim["lean_name"],
                match_terms=tuple(claim.get("match_terms", [])),
            )
            for claim in item["solution_skeleton"]
        )
        problems.append(
            Problem(
                problem_id=item["id"],
                source=item["source"],
                topic=item["topic"],
                difficulty=item["difficulty"],
                prompt=item["problem"],
                final_answer=item["final_answer"],
                solution_skeleton=skeleton,
            )
        )
    return tuple(problems)


def load_sample_runs(path: Path | None = None) -> tuple[ModelRun, ...]:
    runs_path = path or _project_root() / "data" / "sample_runs.json"
    payload = json.loads(runs_path.read_text())
    runs: list[ModelRun] = []
    for run in payload:
        responses = tuple(
            Response(
                problem_id=response["problem_id"],
                final_answer=response["final_answer"],
                claims=tuple(response["claims"]),
            )
            for response in run["responses"]
        )
        runs.append(
            ModelRun(
                model=run["model"],
                prompt_style=run["prompt_style"],
                responses=responses,
            )
        )
    return tuple(runs)
