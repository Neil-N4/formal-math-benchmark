from __future__ import annotations

from pathlib import Path

from .evaluation import RunEvaluation
from .models import Problem


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def render_markdown_report(
    problems: tuple[Problem, ...],
    evaluations: tuple[RunEvaluation, ...],
    output_path: Path | None = None,
) -> Path:
    target = output_path or _project_root() / "outputs" / "report.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    problem_index = {problem.problem_id: problem for problem in problems}

    lines = [
        "# Formal Math Benchmark Report",
        "",
        "## Benchmark Snapshot",
        "",
        f"- Problems: {len(problems)}",
        f"- Topics: {', '.join(sorted({problem.topic for problem in problems}))}",
        "",
        "## Model Results",
        "",
        "| Model | Prompt Style | Answer Accuracy | Claim Recall | Verified Claim Rate | Unsupported Claims |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for run in evaluations:
        lines.append(
            f"| {run.model} | {run.prompt_style} | {run.answer_accuracy:.2%} | {run.claim_recall:.2%} | {run.verified_claim_rate:.2%} | {run.unsupported_claim_count} |"
        )

    for run in evaluations:
        lines.extend(
            [
                "",
                f"## Detailed Results: {run.model} ({run.prompt_style})",
                "",
            ]
        )
        for result in run.problem_results:
            problem = problem_index[result.problem_id]
            lines.extend(
                [
                    f"### {result.problem_id}",
                    "",
                    f"- Topic: {problem.topic}",
                    f"- Difficulty: {problem.difficulty}",
                    f"- Final answer correct: {'yes' if result.final_answer_correct else 'no'}",
                    f"- Covered claims: {', '.join(result.covered_claim_ids) if result.covered_claim_ids else 'none'}",
                    f"- Missing claims: {', '.join(result.missing_claim_ids) if result.missing_claim_ids else 'none'}",
                    f"- Formal verification candidates: {result.verified_claim_candidates}/{result.formalizable_claim_count}",
                    f"- Unsupported claims: {', '.join(result.unsupported_claims) if result.unsupported_claims else 'none'}",
                    "",
                ]
            )

    target.write_text("\n".join(lines))
    return target
