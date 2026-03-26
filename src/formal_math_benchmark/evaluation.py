from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .models import Claim, ModelRun, Problem, Response


@dataclass(frozen=True)
class ProblemEvaluation:
    problem_id: str
    topic: str
    final_answer_correct: bool
    covered_claim_ids: tuple[str, ...]
    missing_claim_ids: tuple[str, ...]
    unsupported_claims: tuple[str, ...]
    verified_claim_candidates: int
    formalizable_claim_count: int


@dataclass(frozen=True)
class RunEvaluation:
    model: str
    prompt_style: str
    answer_accuracy: float
    claim_recall: float
    verified_claim_rate: float
    unsupported_claim_count: int
    problem_results: tuple[ProblemEvaluation, ...]


def _normalize(text: str) -> str:
    return "".join(ch.lower() for ch in text if ch.isalnum())


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 1 or token.isdigit()}


def _claim_matches(claim: Claim, candidate: str) -> bool:
    candidate_words = _tokenize(candidate)
    if claim.match_terms:
        normalized_terms = {_normalize(term) for term in claim.match_terms}
        candidate_normalized = _normalize(candidate)
        hits = sum(1 for term in normalized_terms if term and term in candidate_normalized)
        threshold = max(1, min(len(normalized_terms), 2))
        return hits >= threshold

    reference_words = _tokenize(claim.statement)
    candidate_words = _tokenize(candidate)
    if not reference_words or not candidate_words:
        return False
    overlap = reference_words & candidate_words
    numeric_reference = {token for token in reference_words if token.isdigit()}
    numeric_candidate = {token for token in candidate_words if token.isdigit()}
    numeric_match = not numeric_reference or bool(numeric_reference & numeric_candidate)
    semantic_overlap = len(overlap) >= max(2, min(len(reference_words), len(candidate_words)) // 3)
    return numeric_match and semantic_overlap


def _cover_claims(problem: Problem, response: Response) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], int]:
    covered: list[str] = []
    unsupported: list[str] = []
    verified_candidates = 0

    for claim in problem.solution_skeleton:
        if any(_claim_matches(claim, response_claim) for response_claim in response.claims):
            covered.append(claim.claim_id)
            if claim.formalizable:
                verified_candidates += 1

    for response_claim in response.claims:
        if not any(_claim_matches(claim, response_claim) for claim in problem.solution_skeleton):
            unsupported.append(response_claim)

    missing = [claim.claim_id for claim in problem.solution_skeleton if claim.claim_id not in covered]
    return tuple(covered), tuple(missing), tuple(unsupported), verified_candidates


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def evaluate_runs(problems: Iterable[Problem], runs: Iterable[ModelRun]) -> tuple[RunEvaluation, ...]:
    problem_index = {problem.problem_id: problem for problem in problems}
    evaluations: list[RunEvaluation] = []

    for run in runs:
        problem_results: list[ProblemEvaluation] = []
        answer_hits = 0
        total_covered = 0
        total_required = 0
        total_verified_candidates = 0
        total_formalizable = 0
        total_unsupported = 0

        for response in run.responses:
            problem = problem_index[response.problem_id]
            covered, missing, unsupported, verified_candidates = _cover_claims(problem, response)
            answer_correct = _normalize(response.final_answer) == _normalize(problem.final_answer)
            if answer_correct:
                answer_hits += 1
            total_covered += len(covered)
            total_required += len(problem.solution_skeleton)
            total_verified_candidates += verified_candidates
            total_formalizable += sum(1 for claim in problem.solution_skeleton if claim.formalizable)
            total_unsupported += len(unsupported)
            problem_results.append(
                ProblemEvaluation(
                    problem_id=problem.problem_id,
                    topic=problem.topic,
                    final_answer_correct=answer_correct,
                    covered_claim_ids=covered,
                    missing_claim_ids=missing,
                    unsupported_claims=unsupported,
                    verified_claim_candidates=verified_candidates,
                    formalizable_claim_count=sum(1 for claim in problem.solution_skeleton if claim.formalizable),
                )
            )

        evaluations.append(
            RunEvaluation(
                model=run.model,
                prompt_style=run.prompt_style,
                answer_accuracy=_safe_ratio(answer_hits, len(run.responses)),
                claim_recall=_safe_ratio(total_covered, total_required),
                verified_claim_rate=_safe_ratio(total_verified_candidates, total_formalizable),
                unsupported_claim_count=total_unsupported,
                problem_results=tuple(problem_results),
            )
        )

    return tuple(evaluations)
