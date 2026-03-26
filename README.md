# Formal Math Benchmark & Reasoning Evaluator

Formal Math Benchmark & Reasoning Evaluator is a research-oriented evaluation stack for testing frontier LLMs on olympiad-style mathematics while separating answer accuracy from proof validity.

The project has two layers:

1. A runnable Python pipeline for benchmark management, answer extraction, reasoning-step analysis, Lean 4 proof-obligation generation, and reporting.
2. A Lean 4 scaffold for formally checking selected intermediate claims and reference solutions once Lean is installed locally.

The core thesis is simple: a model can produce the correct final answer while still using invalid or unverifiable reasoning. Standard accuracy benchmarks miss that gap.

## What This Repo Includes

- A small curated benchmark of AMC/AIME-style problems across algebra, number theory, combinatorics, and geometry.
- Structured solution skeletons with explicit claim IDs and proof obligations.
- A Python evaluator that scores:
  - final answer correctness
  - claim coverage
  - claim consistency against the reference skeleton
  - formal-verification readiness
- A Lean 4 code generator that emits theorem stubs and proof placeholders from benchmark data.
- A sample report showing how answer correctness and formal reasoning validity diverge.

## Project Structure

```text
formal-math-benchmark/
├── data/
│   ├── problems.json
│   └── sample_runs.json
├── docs/
│   └── methodology.md
├── lean/
│   ├── FormalMathBenchmark/
│   │   ├── Examples.lean
│   │   └── Generated.lean
│   ├── FormalMathBenchmark.lean
│   ├── lakefile.lean
│   └── lean-toolchain
├── outputs/
│   └── .gitkeep
├── scripts/
│   └── run_demo.py
├── src/
│   └── formal_math_benchmark/
│       ├── __init__.py
│       ├── dataset.py
│       ├── evaluation.py
│       ├── lean_generator.py
│       ├── models.py
│       ├── openai_runner.py
│       └── reporting.py
└── pyproject.toml
```

## Quick Start

Run the demo evaluation:

```bash
python3 scripts/run_demo.py
```

This will:

- load the benchmark
- evaluate two sample model runs
- write a markdown report to `outputs/report.md`
- generate Lean theorem stubs at `lean/FormalMathBenchmark/Generated.lean`

## Lean 4 Setup

Lean is not required for the Python demo, but it is required for formal proof checking.

After installing Lean 4 with `elan`, you can enter the Lean project directory and build:

```bash
cd lean
lake build
```

The generated file `FormalMathBenchmark/Generated.lean` contains theorem stubs derived from the benchmark's proof obligations.

## Evaluation Outputs

The Python pipeline reports:

- `answer_accuracy`: exact-match final answer accuracy
- `claim_recall`: how many required reasoning claims the model explicitly covers
- `verified_claim_rate`: proportion of claims that are ready for formal checking
- `unsupported_claims`: claims that do not map cleanly to the reference proof skeleton
- `hallucinated_claims`: extra steps or lemmas unsupported by the benchmark specification

This allows you to highlight cases where a model reaches the right answer by invalid reasoning.

## OpenAI Integration

`src/formal_math_benchmark/openai_runner.py` includes a minimal adapter for collecting model outputs from the OpenAI Responses API when the `openai` package and credentials are available. The rest of the repo runs offline without external dependencies.

## Why This Project Matters

This benchmark is designed to support research questions such as:

- How often do models produce correct answers for invalid reasons?
- Which math domains are easiest to formalize?
- Which classes of model reasoning errors survive answer-only evaluation?
- How much of a natural-language solution can be converted into proof obligations automatically?

## Resume Framing

Formal Math Benchmark & Reasoning Evaluator | Python, Lean 4, OpenAI API

Built a benchmark of olympiad-style math problems and a verification pipeline that translated model-generated solutions into formal proof obligations in Lean 4, distinguishing correct final answers from logically valid reasoning.
