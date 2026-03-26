from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from formal_math_benchmark import evaluate_runs, load_benchmark, load_sample_runs


def make_model_comparison_figure() -> None:
    problems = load_benchmark()
    runs = load_sample_runs()
    evaluations = evaluate_runs(problems, runs)

    models = [f"{run.model}\n{run.prompt_style}" for run in evaluations]
    answer = [run.answer_accuracy * 100 for run in evaluations]
    verified = [run.verified_claim_rate * 100 for run in evaluations]
    unsupported = [run.unsupported_claim_count for run in evaluations]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    x = range(len(models))
    width = 0.34
    axes[0].bar([i - width / 2 for i in x], answer, width=width, color="#0f766e", label="Answer Accuracy")
    axes[0].bar([i + width / 2 for i in x], verified, width=width, color="#c2410c", label="Verified Claim Rate")
    axes[0].set_ylim(0, 110)
    axes[0].set_ylabel("Percent")
    axes[0].set_title("Answer Accuracy vs Formal Verification Readiness")
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels(models)
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(models, unsupported, color="#334155")
    axes[1].set_title("Unsupported Claims Flagged by the Evaluator")
    axes[1].set_ylabel("Count")
    axes[1].grid(axis="y", alpha=0.25)

    fig.suptitle("Sample Benchmark Evaluation Snapshot", fontsize=14, fontweight="bold")
    fig.tight_layout()

    output = ROOT / "docs" / "images" / "model_comparison.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_problem_breakdown_figure() -> None:
    problems = load_benchmark()

    ids = [problem.problem_id.replace("_", "\n") for problem in problems]
    formalizable = [sum(1 for claim in problem.solution_skeleton if claim.formalizable) for problem in problems]
    total_claims = [len(problem.solution_skeleton) for problem in problems]
    topics = [problem.topic.title() for problem in problems]

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

    axes[0].bar(ids, total_claims, color="#2563eb")
    axes[0].bar(ids, formalizable, color="#93c5fd")
    axes[0].set_title("Proof Obligations per Benchmark Problem")
    axes[0].set_ylabel("Claim Count")
    axes[0].grid(axis="y", alpha=0.25)

    topic_counts: dict[str, int] = {}
    for topic in topics:
        topic_counts[topic] = topic_counts.get(topic, 0) + 1

    axes[1].pie(
        topic_counts.values(),
        labels=topic_counts.keys(),
        autopct="%1.0f%%",
        startangle=110,
        colors=["#0f766e", "#7c3aed", "#c2410c", "#2563eb"],
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    axes[1].set_title("Current Topic Mix")

    fig.suptitle("Benchmark Composition", fontsize=14, fontweight="bold")
    fig.tight_layout()

    output = ROOT / "docs" / "images" / "benchmark_composition.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_model_comparison_figure()
    make_problem_breakdown_figure()
    print("Wrote README figures to docs/images/")


if __name__ == "__main__":
    main()
