from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from formal_math_benchmark import (
    evaluate_runs,
    generate_lean_file,
    load_benchmark,
    load_sample_runs,
    render_markdown_report,
)


def main() -> None:
    problems = load_benchmark()
    runs = load_sample_runs()
    evaluations = evaluate_runs(problems, runs)
    report_path = render_markdown_report(problems, evaluations)
    lean_path = generate_lean_file(problems)

    print(f"Loaded {len(problems)} problems and {len(runs)} model runs.")
    print(f"Wrote markdown report to {report_path}")
    print(f"Generated Lean stubs at {lean_path}")
    for run in evaluations:
        print(
            f"{run.model} [{run.prompt_style}] -> "
            f"answer_accuracy={run.answer_accuracy:.2%}, "
            f"claim_recall={run.claim_recall:.2%}, "
            f"verified_claim_rate={run.verified_claim_rate:.2%}, "
            f"unsupported_claims={run.unsupported_claim_count}"
        )


if __name__ == "__main__":
    main()
