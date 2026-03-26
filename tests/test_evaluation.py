from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from formal_math_benchmark import evaluate_runs, load_benchmark, load_sample_runs


def test_sample_runs_evaluate_with_expected_accuracy_profile() -> None:
    problems = load_benchmark()
    runs = load_sample_runs()
    results = evaluate_runs(problems, runs)

    assert len(results) == 2
    mini, full = results

    assert mini.model == "gpt-4.1-mini"
    assert mini.answer_accuracy == 0.75
    assert full.model == "gpt-4.1"
    assert full.answer_accuracy == 1.0


def test_number_theory_problem_is_scored_incorrect_for_bad_answer() -> None:
    problems = load_benchmark()
    runs = load_sample_runs()
    results = evaluate_runs(problems, runs)

    mini = results[0]
    number_theory = next(
        problem_result for problem_result in mini.problem_results if problem_result.problem_id == "number_theory_divisibility"
    )
    assert not number_theory.final_answer_correct
    assert "c1" in number_theory.covered_claim_ids
