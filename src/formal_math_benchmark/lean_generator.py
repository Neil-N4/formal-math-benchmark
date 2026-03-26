from __future__ import annotations

from pathlib import Path

from .models import Problem


HEADER = """import Mathlib.Data.Int.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.NormNum
import FormalMathBenchmark.Examples

namespace FormalMathBenchmark.Generated

"""

FOOTER = """
end FormalMathBenchmark.Generated
"""


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _sanitize_comment(text: str) -> str:
    return text.replace("/-", "").replace("-/", "")


THEOREM_TEMPLATES: dict[tuple[str, str], tuple[str, list[str]]] = {
    (
        "algebra_linear_system",
        "sum_sq_identity",
    ): (
        "theorem {name} (x y : Int) : x^2 + y^2 = (x + y)^2 - 2 * x * y := by",
        ["  simpa [mul_comm, mul_left_comm, mul_assoc] using FormalMathBenchmark.sum_sq_identity x y"],
    ),
    (
        "algebra_linear_system",
        "sum_sq_substitution",
    ): (
        "theorem {name} (x y : Int) (h : x + y = 10) : (x + y)^2 = 100 := by",
        ["  calc", "    (x + y)^2 = (10 : Int)^2 := by simpa [h]", "    _ = 100 := by norm_num"],
    ),
    (
        "algebra_linear_system",
        "algebra_linear_system_final",
    ): (
        "theorem {name} (x y : Int) (hs : x + y = 10) (hxy : x * y = 21) : x^2 + y^2 = 58 := by",
        [
            "  calc",
            "    x^2 + y^2 = (x + y)^2 - 2 * x * y := by",
            "      simpa [mul_comm, mul_left_comm, mul_assoc] using FormalMathBenchmark.sum_sq_identity x y",
            "    _ = (10 : Int)^2 - 2 * (x * y) := by",
            "      rw [hs]",
            "      ring",
            "    _ = (10 : Int)^2 - 2 * 21 := by rw [hxy]",
            "    _ = 58 := by norm_num",
        ],
    ),
    (
        "number_theory_divisibility",
        "mod_reduce_six",
    ): (
        "theorem {name} : 6 % 5 = 1 := by",
        ["  norm_num"],
    ),
    (
        "number_theory_divisibility",
        "mod_expression_rewrite",
    ): (
        "theorem {name} : (6^4 + 6^3 + 6^2 + 6 + 1) % 5 = (1^4 + 1^3 + 1^2 + 1 + 1 : Nat) % 5 := by",
        ["  norm_num"],
    ),
    (
        "number_theory_divisibility",
        "mod_compute_final",
    ): (
        "theorem {name} : (1^4 + 1^3 + 1^2 + 1 + 1 : Nat) % 5 = 0 := by",
        ["  norm_num"],
    ),
    (
        "number_theory_divisibility",
        "geometric_series_mod",
    ): (
        "theorem {name} : (6^4 + 6^3 + 6^2 + 6 + 1 : Nat) % 5 = 0 := by",
        ["  norm_num"],
    ),
    (
        "combinatorics_handshakes",
        "handshake_pairs",
    ): (
        "theorem {name} : Nat.choose 8 2 = 28 := by",
        ["  native_decide"],
    ),
    (
        "combinatorics_handshakes",
        "handshake_choose",
    ): (
        "theorem {name} : Nat.choose 8 2 = 28 := by",
        ["  native_decide"],
    ),
    (
        "combinatorics_handshakes",
        "handshake_final",
    ): (
        "theorem {name} : Nat.choose 8 2 = 28 := by",
        ["  native_decide"],
    ),
    (
        "geometry_triangle_angle",
        "triangle_angle_sum",
    ): (
        "theorem {name} : (50 + 60 + 70 : Int) = 180 := by",
        ["  norm_num"],
    ),
    (
        "geometry_triangle_angle",
        "triangle_angle_final",
    ): (
        "theorem {name} : (180 - 50 - 60 : Int) = 70 := by",
        ["  norm_num"],
    ),
}


def _render_claim(problem_id: str, lean_name: str, theorem_name: str) -> list[str]:
    signature, proof_lines = THEOREM_TEMPLATES[(problem_id, lean_name)]
    return [signature.format(name=theorem_name), *proof_lines, ""]


def _render_problem(problem: Problem) -> str:
    chunks = [f"/- Problem: {problem.problem_id}", f"   Topic: {problem.topic}", f"   Prompt: {_sanitize_comment(problem.prompt)}", "-/\n"]
    for claim in problem.solution_skeleton:
        theorem_name = f"{problem.problem_id}_{claim.lean_name}"
        chunks.append(f"/- Claim {claim.claim_id}: {_sanitize_comment(claim.statement)} -/")
        chunks.extend(_render_claim(problem.problem_id, claim.lean_name, theorem_name))
    return "\n".join(chunks)


def generate_lean_file(problems: tuple[Problem, ...], output_path: Path | None = None) -> Path:
    target = output_path or _project_root() / "lean" / "FormalMathBenchmark" / "Generated.lean"
    target.parent.mkdir(parents=True, exist_ok=True)
    body = "\n\n".join(_render_problem(problem) for problem in problems)
    target.write_text(HEADER + body + FOOTER)
    return target
